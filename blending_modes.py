import numpy as np

def scale_down(base: np.ndarray, top: np.ndarray) -> np.ndarray:
    return base / 255, top / 255


def scale_up(img: np.ndarray) -> np.ndarray:
    return (img * 255).astype(np.uint8)


def blend_overlay(base: np.ndarray, top: np.ndarray) -> np.ndarray:
    mask = base >= 0.5
    result = np.zeros_like(base, dtype=float)
    result[~mask] = (mult_2 := (2 * base * top))[~mask]
    result[mask] = (2 * base + 2 * top - mult_2 - 1)[mask]
    return result


def blend_hard_light(base: np.ndarray, top: np.ndarray) -> np.ndarray:
    return blend_overlay(top, base)


def blend_multiply(base: np.ndarray, top: np.ndarray) -> np.ndarray:
    return base * top


def blend_screen(base: np.ndarray, top: np.ndarray) -> np.ndarray:
    return base + top - base * top


def blend_soft_light(base: np.ndarray, top: np.ndarray) -> np.ndarray:
    return (1 - 2 * top) * base**2 + 2 * base * top


def blend_color_burn(base: np.ndarray, top: np.ndarray) -> np.ndarray:
    result = np.zeros_like(base, dtype=float)
    mask = top != 0.0
    result[mask] = np.maximum(0, 1 - (1 - base[mask]) / top[mask])
    return result


def blend_color_dodge(base: np.ndarray, top: np.ndarray) -> np.ndarray:
    result = np.ones_like(base, dtype=float)
    mask = top != 1.0
    result[mask] = np.minimum(1, base[mask] / (1 - top[mask]))
    return result


def blend_lighten(base: np.ndarray, top: np.ndarray) -> np.ndarray:
    return np.maximum(base, top)


def blend_darken(base: np.ndarray, top: np.ndarray) -> np.ndarray:
    return np.minimum(base, top)


def blend_divide(base: np.ndarray, top: np.ndarray) -> np.ndarray:
    result = np.ones_like(base, dtype=float)
    mask = top != 0.0
    result[mask] = base[mask] / top[mask]
    return np.minimum(1.0, result)


def blend_subtract(base: np.ndarray, top: np.ndarray) -> np.ndarray:
    return np.maximum(0, base - top)


def blend_linear_dodge(base: np.ndarray, top: np.ndarray) -> np.ndarray:
    return np.minimum(1, base + top)


def blend_difference(base: np.ndarray, top: np.ndarray) -> np.ndarray:
    return np.abs(base - top)


def blend_dissolve(base: np.ndarray, top: np.ndarray) -> np.ndarray:
    mask = np.random.choice([False, True], size=base.shape[:2])
    result = np.zeros_like(base, dtype=float)
    result[mask] = base[mask]
    result[~mask] = top[~mask]
    return result


def blend_normal(base: np.ndarray, top: np.ndarray) -> np.ndarray:
    return top


def blend_linear_burn(base: np.ndarray, top: np.ndarray) -> np.ndarray:
    return np.maximum(0, base + top - 1.0)


def blend_exclusion(base: np.ndarray, top: np.ndarray) -> np.ndarray:
    return base + top - 2 * base * top


def blend_linear_light(base: np.ndarray, top: np.ndarray) -> np.ndarray:
    return np.clip(base + 2 * top - 1, 0.0, 1.0)


def blend_vivid_light(base: np.ndarray, top: np.ndarray) -> np.ndarray:
    result = np.zeros_like(base, dtype=float)
    mask = top < 0.5
    result[mask] = blend_color_burn(base, 2 * top)[mask]
    result[~mask] = blend_color_dodge(base, 2 * top - 1)[~mask]
    return result


def blend_pin_light(base: np.ndarray, top: np.ndarray) -> np.ndarray:
    result = np.zeros_like(base, dtype=float)
    mask = top < 0.5
    result[mask] = np.minimum(base, 2 * top)[mask]
    result[~mask] = np.maximum(base, 2 * top - 1)[~mask]
    return result


def blend_hard_mix(base: np.ndarray, top: np.ndarray) -> np.ndarray:
    return (base + top) >= 1.0


def blend_reflect(base: np.ndarray, top: np.ndarray) -> np.ndarray:
    result = np.ones_like(base, dtype=float)
    mask = top != 1.0
    result[mask] = np.minimum(1.0, base[mask] ** 2 / (1 - top[mask]))
    return result


def blend_grain_merge(base: np.ndarray, top: np.ndarray) -> np.ndarray:
    return np.clip(base - top + 0.5, 0, 1)


def blend_grain_extract(base: np.ndarray, top: np.ndarray) -> np.ndarray:
    return np.clip(base + top - 0.5, 0, 1)
