from shop.models import Product
from .forms import ReviewForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .forms import ReviewFeedbackForm
from .models import Review, ReviewFeedback


@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    existing_review = Review.objects.filter(product=product, user=request.user).first()
    if existing_review:
        messages.warning(request, "Вы уже оставили отзыв на этот товар.")
        return redirect('product_detail', pk=product.id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, "Спасибо за ваш отзыв!")
            return redirect('product_detail', pk=product.id)
    else:
        form = ReviewForm()

    return render(request, 'reviews/review_form.html', {'form': form, 'product': product})


@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if review.user != request.user:
        return HttpResponseForbidden("Вы не можете редактировать этот отзыв.")

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('product_detail', pk=review.product.id)
    else:
        form = ReviewForm(instance=review)

    return render(request, 'reviews/review_form.html', {'form': form, 'product': review.product})

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    if request.method == 'POST':
        review.delete()
        return redirect('product_detail', pk=review.product.id)
    return render(request, 'reviews/review_confirm_delete.html', {
        'review': review,
        'hide_messages': True,
    })

@login_required
def helpful_vote(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    vote = request.POST.get('vote')

    if vote == 'yes':
        review.helpful_yes += 1
    elif vote == 'no':
        review.helpful_no += 1
    else:
        return redirect('product_detail', pk=review.product.id)

    review.save()
    return redirect('product_detail', pk=review.product.id)

@login_required
def review_feedback(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    existing_feedback = ReviewFeedback.objects.filter(review=review, user=request.user).first()

    if request.method == 'POST':
        form = ReviewFeedbackForm(request.POST, instance=existing_feedback)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.review = review
            feedback.user = request.user
            feedback.save()
            review.helpful_yes = review.feedbacks.filter(was_helpful=True).count()
            review.helpful_no = review.feedbacks.filter(was_helpful=False).count()
            review.save()

            return redirect('product_detail', pk=review.product.id)
    else:
        form = ReviewFeedbackForm(instance=existing_feedback)



