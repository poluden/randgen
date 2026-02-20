from rng import generate

def test_generate_ranges():
    r = generate()
    assert 0 <= r.rand_a < 1_000_000
    assert 0 <= r.calc_b < 1_000_000
    assert isinstance(r.nonce, str) and len(r.nonce) == 16
    assert "Z" in r.ts_iso

def test_seed_hint_changes_output_probably():
    r1 = generate(seed_hint="a")
    r2 = generate(seed_hint="b")
    # не 100%, але практично завжди різні
    assert (r1.calc_b, r1.rand_a, r1.nonce) != (r2.calc_b, r2.rand_a, r2.nonce)