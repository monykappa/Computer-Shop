from shared_imports import *



def create_order(user, items, total_price):
    # Get the user's current address
    current_address = Address.objects.filter(user=user).last()

    if current_address:
        # Create a new OrderAddress based on the current address
        order_address = OrderAddress.objects.create(
            address1=current_address.address1,
            address2=current_address.address2,
            city=current_address.city,
            province=current_address.province,
            phone=current_address.phone
        )

        # Create the order
        order = OrderHistory.objects.create(
            user=user,
            order_address=order_address,
            total_price=total_price,
            status=OrderStatus.PENDING
        )

        # Create OrderHistoryItems
        for item in items:
            OrderHistoryItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                price=item['price']
            )

        return order
    else:
        # Handle the case where the user doesn't have an address
        raise ValueError("User does not have a valid address")
    
    
# Check if user logged-in, in order to add product to cart
class CheckLoginStatusView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return JsonResponse({"logged_in": True})
        else:
            return JsonResponse({"logged_in": False})
        


logger = logging.getLogger(__name__)


@method_decorator(login_required, name='dispatch')
class AddToCartView(View):
    def post(self, request, slug):
        logger.info(f"AddToCartView post method called for slug: {slug}")
        logger.info(f"User: {request.user}")
        try:
            product = get_object_or_404(Product, slug=slug)
            stock = get_object_or_404(Stock, product=product)
            logger.info(f"Product found: {product}, Stock: {stock}")

            quantity = int(request.POST.get("quantity", 1))
            logger.info(f"Requested Quantity: {quantity}")

            # Check if the requested quantity exceeds available stock
            if quantity > stock.quantity:
                return JsonResponse({'error': f'Only {stock.quantity} units available in stock.'}, status=400)

            with transaction.atomic():
                # Get or create an order
                order, created = Order.objects.get_or_create(
                    user=request.user,
                    status=OrderStatus.PENDING
                )
                logger.info(f"Order found or created: {order}, created: {created}")

                # Get or create a cart item
                cart_item, created = CartItem.objects.get_or_create(
                    order=order,
                    product=product,
                )
                if created:
                    cart_item.quantity = quantity
                    logger.info(f"CartItem created: {cart_item}")
                else:
                    cart_item.quantity += quantity
                    logger.info(f"CartItem updated: {cart_item}")

                cart_item.save()

                # Deduct stock after ensuring the cart item was correctly updated
                if quantity <= stock.quantity:
                    stock.quantity -= quantity
                    stock.save()
                    logger.info(f"Stock updated: {stock}")
                else:
                    return JsonResponse({'error': f'Insufficient stock. Only {stock.quantity} units available.'}, status=400)

                # Recalculate the total price of the order
                order.calculate_total_price()
                logger.info(f"Order total price calculated: {order.total_price}")

            return JsonResponse({'message': 'Product added to cart successfully.'})

        except Exception as e:
            logger.error(f"Error adding product to cart: {e}")
            return JsonResponse({'error': str(e)}, status=400)


        

class CartDetailView(TemplateView):
    template_name = "cart/cart_auth.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_authenticated'] = self.request.user.is_authenticated
        return context


logger = logging.getLogger(__name__)

class PublicCartAPIView(APIView):
    permission_classes = []  # No specific permissions required

    def get(self, request):
        try:
            logger.info("Fetching cart for user: %s", request.user)
            if request.user.is_authenticated:
                order = Order.objects.filter(user=request.user, created_at__isnull=False).first()
                
                if not order:
                    logger.info("No active order found for user: %s", request.user)
                    return Response({
                        "cart_items": [],
                        "total_price": 0,
                        "user_authenticated": True,
                        "user_has_address": False,
                    })
                
                logger.info("Order found: %s", order)
                
                cart_items = order.cartitem_set.all().select_related('product').prefetch_related(
                    Prefetch('product__images', queryset=ProductImage.objects.all())
                )
                serializer = CartItemSerializer(cart_items, many=True)
                total_price = order.total_price
                
                # Check if UserProfile exists and has an address
                user_has_address = False
                if hasattr(request.user, "userprofile"):
                    user_profile = request.user.userprofile
                    user_has_address = any([
                        getattr(user_profile, 'address', None),
                        getattr(user_profile, 'address1', None),
                        getattr(user_profile, 'street_address', None)
                    ])
                
                logger.info("Cart items serialized successfully")

                return Response({
                    "cart_items": serializer.data,
                    "total_price": total_price,
                    "user_authenticated": True,
                    "user_has_address": user_has_address,
                })
            else:
                logger.warning("User not authenticated")
                return Response({
                    "cart_items": [],
                    "total_price": 0,
                    "user_authenticated": False,
                    "message": "You need to sign in to view your cart.",
                }, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            logger.error("Error fetching cart data: %s", str(e), exc_info=True)
            return Response({
                "error": str(e),
                "cart_items": [],
                "total_price": 0,
                "user_authenticated": request.user.is_authenticated,
                "message": "Failed to fetch cart data.",
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, item_id):
        try:
            item = get_object_or_404(CartItem, id=item_id)
            new_quantity = request.data.get('quantity')
            if new_quantity > item.product.stock:
                return Response({
                    "error": f"Cannot increase quantity beyond available stock ({item.product.stock})"
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Update item quantity
            item.quantity = new_quantity
            item.save()
            # Calculate the new subtotal and total
            subtotal = item.quantity * item.product.price
            total_price = sum([i.quantity * i.product.price for i in item.order.cartitem_set.all()])
            item_count = item.order.cartitem_set.count()

            return Response({
                "item_id": item_id,
                "quantity": new_quantity,
                "subtotal": subtotal,
                "total_price": total_price,
                "item_count": item_count
            })
        except Exception as e:
            logger.error("Error updating cart item: %s", str(e), exc_info=True)
            return Response({
                "error": str(e),
                "message": "Failed to update cart item."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class CartAPIView(APIView):
    permission_classes = [IsSuperAdmin]

    def get(self, request):
        try:
            order = Order.objects.get(user=request.user, created_at__isnull=False)
            cart_items = order.cartitem_set.all().select_related('product').prefetch_related(
                Prefetch('product__images', queryset=ProductImage.objects.all())
            )
            serializer = CartItemSerializer(cart_items, many=True)
            total_price = order.total_price
            user_has_address = (
                hasattr(request.user, "userprofile")
                and request.user.userprofile.address1 is not None
            )
            
            return Response({
                "cart_items": serializer.data,
                "total_price": total_price,
                "user_authenticated": True,
                "user_has_address": user_has_address,
            })
        except Order.DoesNotExist:
            return Response({
                "cart_items": [],
                "total_price": 0,
                "user_authenticated": True,
                "user_has_address": False,
            })
        except Exception as e:
            return Response({
                "error": str(e),
                "cart_items": [],
                "total_price": 0,
                "user_authenticated": False,
                "message": "Failed to fetch cart data.",
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            
class RemoveFromCartView(DeleteView):
    model = CartItem
    success_url = reverse_lazy('orders:cart_detail')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        order = self.object.order
        item_id = self.object.id
        self.object.delete()

        # Recalculate the total price after removing the item
        order_items = order.cartitem_set.all()
        total_price = sum(item.subtotal for item in order_items)
        order.total_price = total_price
        order.save()

        # Calculate the remaining item count
        item_count = order_items.count()

        return JsonResponse({
            'item_id': item_id,
            'total_price': float(total_price),
            'item_count': item_count,
        })
        
        
class UpdateCartQuantityView(View):
    def post(self, request, item_id):
        print(f"Received request to update item_id: {item_id}")
        cart_item = get_object_or_404(CartItem, id=item_id)
        quantity = int(request.POST.get('quantity', 1))
        print(f"Updating quantity to: {quantity}")

        # Fetch the related stock
        stock = cart_item.product.stock

        # Check if quantity exceeds available stock
        if quantity > stock.quantity:
            return JsonResponse({'error': f'Cannot exceed stock quantity of {stock.quantity}'}, status=400)
        
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
            order = cart_item.order
            order_items = order.cartitem_set.all()
            order.total_price = sum(item.subtotal for item in order_items)
            order.save()
            return JsonResponse({
                'item_id': cart_item.id,
                'quantity': cart_item.quantity,
                'subtotal': float(cart_item.subtotal),
                'total_price': float(order.total_price),
            })
        else:
            return JsonResponse({'error': 'Invalid quantity'}, status=400)


@login_required
def pay_with_paypal(request):
    user_profile = get_object_or_404(Address, user=request.user)

    # Check if the user has confirmed their address
    if not user_profile.address_confirmed:
        # Redirect the user to the address confirmation view
        return redirect("orders:confirm_address")

    # Get the user's order and the associated cart items
    try:
        order = Order.objects.get(user=request.user, created_at__isnull=False)
        if not order.order_address:
            return redirect("orders:confirm_address")

        cart_items = order.cartitem_set.all()
        order.calculate_total_price()
        total_price = order.total_price
    except Order.DoesNotExist:
        return redirect("orders:cart_detail")

    response = render(
        request,
        "payment/pay_with_paypal.html",
        {"cart_items": cart_items, "total_price": total_price},
    )

    # Reset the address_confirmed attribute to False
    user_profile.address_confirmed = False
    user_profile.save()

    return response


@login_required
def confirm_address(request):
    try:
        order = Order.objects.get(user=request.user, created_at__isnull=False)
        cart_items = order.cartitem_set.all()
        if not cart_items:
            return redirect("orders:cart_detail")
    except Order.DoesNotExist:
        return redirect("orders:cart_detail")

    user_address, created = Address.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = AddressForm(request.POST, instance=user_address)
        if form.is_valid():
            user_address = form.save()
            
            # Create OrderAddress if it doesn't exist
            order_address, created = OrderAddress.objects.get_or_create(
                address1=user_address.address1,
                address2=user_address.address2,
                city=user_address.city,
                province=user_address.province,
                phone=user_address.phone
            )
            
            # Associate OrderAddress with Order
            order.order_address = order_address
            order.save()
            
            # Mark address as confirmed
            user_profile = get_object_or_404(Address, user=request.user)
            user_profile.address_confirmed = True
            user_profile.save()
            
            return redirect("orders:pay_with_paypal")
    else:
        form = AddressForm(instance=user_address)

    return render(request, "confirm/confirm_address.html", {"form": form})


def send_order_confirmation_email(user_email, order_id, total_price, order_address, order_items):
    subject = 'Order Confirmation'
    
    context = {
        'order_id': order_id,
        'total_price': total_price,
        'order_address': order_address,
        'order_items': order_items,
    }
    
    html_message = render_to_string('order/order_confirmation_email.html', context)
    
    try:
        email = EmailMessage(
            subject,
            html_message,
            from_email=settings.EMAIL_HOST_USER,
            to=[user_email]
        )
        email.content_subtype = 'html'
        email.send()
        logger.info(f"Order confirmation email sent to {user_email}")
    except Exception as e:
        logger.error(f"Failed to send email: {e}")


    

@method_decorator(login_required, name="dispatch")
class ClearCartView(View):
    def post(self, request, *args, **kwargs):
        # Get cart items
        cart_items = CartItem.objects.filter(order__user=request.user)
        
        # Calculate total
        total = sum(item.subtotal for item in cart_items)
        
        # Create OrderHistory
        order_history = OrderHistory.objects.create(
            user=request.user,
            total_price=total
        )
        
        # Save items to OrderHistoryItem
        for item in cart_items:
            OrderHistoryItem.objects.create(
                order_history=order_history,
                product=item.product,
                quantity=item.quantity,
                subtotal=item.subtotal
            )
        
        # Clear cart
        CartItem.objects.filter(order__user=request.user).delete()
        
        # Create or get OrderAddress instance from user's profile
        user_profile = get_object_or_404(Address, user=request.user)
        order_address_instance, created = OrderAddress.objects.get_or_create(
            address1=user_profile.address1,
            address2=user_profile.address2,
            city=user_profile.city,
            province=user_profile.province,
            phone=user_profile.phone
        )
        
        # Associate OrderAddress with OrderHistory
        order_history.order_address = order_address_instance
        order_history.save()
        
        # Prepare the email
        order_items_details = [
            {
                'product_name': item.product.name,
                'product_model': item.product.model,
                'product_year': item.product.year,
                'quantity': item.quantity,
                'subtotal': item.subtotal
            }
            for item in cart_items
        ]
        
        send_order_confirmation_email(
            user_email=request.user.email,
            order_id=order_history.id,
            total_price=order_history.total_price,
            order_address=f"{order_address_instance.address1}, {order_address_instance.city}, {order_address_instance.province}",
            order_items=order_items_details
        )
        
        # Redirect to success page
        return redirect("orders:payment_complete")





@method_decorator(login_required, name="dispatch")
class PaymentCompleteView(TemplateView):
    template_name = "payment/payment_completed.html"

    def get(self, request, *args, **kwargs):
        # Retrieve the latest order history for the current user
        order_history = (
            OrderHistory.objects.filter(user=request.user).order_by("-id").first()
        )
        if not order_history:
            return redirect("orders:cart_detail")

        # Ensure that the QR code is generated only if it doesn't exist already
        if not order_history.qr_code:
            # Generate the QR code for the OrderHistory instance
            order_history.generate_qr_code(request)

        # Debugging: Print the QR code URL
        print(order_history.qr_code.url)

        # Retrieve order history items
        order_history_items = OrderHistoryItem.objects.filter(
            order_history=order_history
        )

        context = {
            "order_history": order_history,
            "order_history_items": order_history_items,
        }

        return self.render_to_response(context)



class OrderHistoryView(LoginRequiredMixin, ListView):
    template_name = "order/order_history.html"
    model = OrderHistory
    context_object_name = "orders"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pending_orders'] = OrderHistory.objects.filter(user=self.request.user, status='Pending').order_by('-ordered_date')
        context['completed_orders'] = OrderHistory.objects.filter(user=self.request.user, status='Completed').order_by('-ordered_date')
        context['cancelled_orders'] = OrderHistory.objects.filter(user=self.request.user, status='Cancelled').order_by('-ordered_date')
        return context

class OrderDetailView(LoginRequiredMixin, DetailView):
    template_name = "order/order_detail.html"
    model = OrderHistory
    context_object_name = "order"
    pk_url_kwarg = "order_id"

    def dispatch(self, request, *args, **kwargs):
        # Get the order object
        order = self.get_object()
        
        # Check if the logged-in user is the owner of the order
        if order.user != request.user:
            return render(request, "unauthorize/unauthorized_access.html")  # Render unauthorized access template
        
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.get_object()
        context["qr_code_url"] = order.qr_code.url if order.qr_code else None
        return context

class OrderHistoryImageView(View):
    def dispatch(self, request, *args, **kwargs):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return render(request, "unauthorize/unauthorized_access.html") 
        
        # Get the order history object
        order_history = get_object_or_404(OrderHistory, id=self.kwargs['order_history_id'])
        
        # Check if the logged-in user is the purchaser
        if order_history.user != request.user:
            return render(request, "unauthorize/unauthorized_access.html")
        
        return super().dispatch(request, *args, **kwargs)
    def get(self, request, order_history_id):
        order_history = get_object_or_404(OrderHistory, id=order_history_id)

        # Create a new image with a white background and increased size
        img = Image.new("RGB", (1200, 1500), color="white")  # Increased image size
        d = ImageDraw.Draw(img)

        # Load the font with an increased size
        try:
            font_size = 24  # Increased font size
            font = ImageFont.truetype("arial.ttf", font_size)
        except IOError:
            font = ImageFont.load_default()

        phnom_penh_timezone = pytz.timezone("Asia/Phnom_Penh")
        ordered_date_phnom_penh = timezone.localtime(
            order_history.ordered_date, timezone=phnom_penh_timezone
        )
        ordered_date_formatted = ordered_date_phnom_penh.strftime("%I:%M %p")

        # Define the texts to be written on the image
        texts = [
            f"Khmer Empire Shop\n",
            f"Order No: {order_history.id}",
            f"Purchased by: {order_history.user.username}",
            f"Ordered Date: {ordered_date_formatted}",
        ]

        # Collect order items information
        order_history_items = OrderHistoryItem.objects.filter(order_history=order_history).select_related('product').prefetch_related('product__images')


        # Calculate y-position for the first text
        y = 150  # Increased y position
        line_height = 40  # Increased line height

        # Draw each text centered on the image
        for text in texts:
            text_width, text_height = d.textbbox((0, 0), text, font=font)[2:4]
            x = (img.width - text_width) // 2  # Center the text horizontally
            d.text((x, y), text, font=font, fill="black")
            y += line_height

        table_headers = ["Product Name", "Model", "Year", "Qty", "Price"]

        # Define the desired margin size
        margin_size = 50

        # Calculate cell width with added margin
        cell_width = (img.width - (margin_size * 2)) // len(table_headers)

        # Draw the table headers

        table_y = y + 100  # Set the starting y-position for the table
        row_height = 40  # Set the row height

        # Draw horizontal line for the top of the table
        d.line([(0, table_y), (img.width, table_y)], fill="black", width=2)

        # Draw table headers
        for i, header in enumerate(table_headers):
            x = (
                margin_size
                + i * cell_width
                + (cell_width - d.textbbox((0, 0), header, font=font)[2]) // 2
            )
            d.text((x, table_y), header, font=font, fill="black")

        # Draw horizontal line for the bottom of the header row
        d.line(
            [(0, table_y + row_height), (img.width, table_y + row_height)],
            fill="black",
            width=2,
        )

        # Define the desired padding between rows
        row_padding = 50
        # Maintain the original row height
        row_height = 90

        # Draw table rows for each product
        for row_index, item in enumerate(order_history_items, start=1):
            row_y = table_y + (row_index * row_height) + (row_index - 1) * row_padding
            x_offset = margin_size
            # Draw product name, model, year
            product_details = [
                item.product.name,
                item.product.model,
                str(item.product.year),
            ]
            for col_index, text in enumerate(product_details):
                x = (
                    margin_size
                    + col_index * cell_width
                    + (cell_width - d.textbbox((0, 0), text, font=font)[2]) // 2
                )
                d.text((x, row_y), text, font=font, fill="black")
                x_offset += cell_width
            # Draw quantity and price
            x_qty = (
                margin_size
                + 3 * cell_width
                + (cell_width - d.textbbox((0, 0), str(item.quantity), font=font)[2])
                // 2
            )
            d.text((x_qty, row_y), str(item.quantity), font=font, fill="black")
            x_price = (
                margin_size
                + 4 * cell_width
                + (
                    cell_width
                    - d.textbbox((0, 0), f"${item.subtotal:.2f}", font=font)[2]
                )
                // 2
            )
            d.text((x_price, row_y), f"${item.subtotal:.2f}", font=font, fill="black")

            # Draw horizontal line to separate rows
            if row_index < len(order_history_items):
                d.line(
                    [(0, row_y + row_height), (img.width, row_y + row_height)],
                    fill="black",
                    width=1,
                )
            else:
                d.line(
                    [
                        (0, row_y + row_height + row_padding),
                        (img.width, row_y + row_height + row_padding),
                    ],
                    fill="black",
                    width=1,
                )

        # Increase font size for total price
        total_price_font_size = 36

        # Load the font with the increased size for total price
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
            total_price_font = ImageFont.truetype("arial.ttf", total_price_font_size)
        except IOError:
            font = ImageFont.load_default()

        # Convert the image to bytes and return it as a response
        buffer = BytesIO()

        # Calculate total price
        total_price = sum(item.subtotal for item in order_history_items)
        total_price_text = f"Total Price: ${total_price:.2f}"

        # Calculate the position of the total price text at the bottom of the image with added margin
        total_price_width, total_price_height = d.textbbox(
            (0, 0), total_price_text, font=total_price_font
        )[2:4]
        total_price_x = (
            margin_size + (img.width - (margin_size * 2) - total_price_width) // 2
        )
        total_price_y = (
            img.height - total_price_height - 50
        )  # Adjust the vertical position as needed

        # Draw total price text with the increased font size
        d.text(
            (total_price_x, total_price_y),
            total_price_text,
            font=total_price_font,
            fill="red",
        )

        # Save the image to the buffer
        img.save(buffer, format="PNG")
        buffer.seek(0)

        # Return the image as an HTTP response
        response = HttpResponse(buffer.getvalue(), content_type="image/png")
        return response

