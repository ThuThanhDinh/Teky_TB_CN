from django.db.models import Sum
from .models import Rank, Voucher, Cart


def voucher_context(request):
    """Provide user's total spent, rank, and vouchers from DB for templates.

    This function will ensure Rank entries exist with the thresholds the user requested
    (Silver=1_000_000, Gold=3_000_000, Diamond=5_000_000) and will return vouchers grouped
    by rank and the list of vouchers applicable to the authenticated user. Disabled vouchers
    are still returned but templates can mark them as disabled.
    """
    context = {}
    user = getattr(request, 'user', None)

    # ensure rank entries exist
    rank_defs = [
        ('Silver', 1000000),
        ('Gold', 3000000),
        ('Diamond', 5000000),
    ]
    for name, thresh in rank_defs:
        Rank.objects.get_or_create(name=name, defaults={'threshold': thresh})

    # compute total spent across completed carts
    total = 0
    if user and getattr(user, 'is_authenticated', False):
        try:
            customer = user.customer
            carts = customer.cart_set.filter(completed=True)
            for cart in carts:
                try:
                    total += cart.get_cart_total
                except Exception:
                    pass
        except Exception:
            total = 0

    # determine user rank based on Rank thresholds (highest first)
    ranks = list(Rank.objects.all().order_by('-threshold'))
    user_rank = None
    for r in ranks:
        if total >= r.threshold:
            user_rank = r.name
            break
    if user_rank is None and ranks:
        user_rank = ranks[-1].name

    # fetch all vouchers
    all_vouchers = Voucher.objects.select_related().prefetch_related('ranks').all()

    # group by rank name
    vouchers_by_rank = {}
    for v in all_vouchers:
        for r in v.ranks.all():
            vouchers_by_rank.setdefault(r.name, []).append(v)

    # applicable vouchers for this user rank
    applicable_vouchers = []
    if user and user.is_authenticated and user_rank:
        applicable_vouchers = [v for v in all_vouchers if any(r.name == user_rank for r in v.ranks.all())]

    context.update({
        'user_total_spent': total,
        'user_rank': user_rank,
        'applicable_vouchers': applicable_vouchers,
        'rank_thresholds': {r.name: r.threshold for r in Rank.objects.all()},
        'vouchers_by_rank': vouchers_by_rank,
        'all_vouchers': list(all_vouchers),
    })
    return context
