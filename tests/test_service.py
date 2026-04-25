from aeza_monitor.models import PromoData
from aeza_monitor.service import detect_event


def test_detect_event_promo_found():
    current = PromoData(found=True, location="Stockholm", plan_code="SWE-PROMO", price="1.99 €")

    assert detect_event(current, None) == "promo_found"


def test_detect_event_promo_changed():
    previous = PromoData(found=True, location="Stockholm", plan_code="SWE-PROMO", price="1.99 €")
    current = PromoData(found=True, location="Vienna", plan_code="VIE-PROMO", price="2.49 €")

    assert detect_event(current, previous) == "promo_changed"


def test_detect_event_promo_lost():
    previous = PromoData(found=True, location="Stockholm", plan_code="SWE-PROMO", price="1.99 €")
    current = PromoData(found=False, reason="Promo not found")

    assert detect_event(current, previous) == "promo_lost"


def test_detect_event_no_change():
    previous = PromoData(found=True, location="Stockholm", plan_code="SWE-PROMO", price="1.99 €")
    current = PromoData(found=True, location="Stockholm", plan_code="SWE-PROMO", price="1.99 €")

    assert detect_event(current, previous) == "no_change"
