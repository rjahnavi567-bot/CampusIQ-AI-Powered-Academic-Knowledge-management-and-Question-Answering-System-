import cv2
import numpy as np


WHITE_THRESHOLD = 245
BLACK_THRESHOLD = 10


# --------------------------------------------------
# Blur
# --------------------------------------------------

def compute_blur(gray):

    return float(
        cv2.Laplacian(
            gray,
            cv2.CV_64F
        ).var()
    )


# --------------------------------------------------
# Noise
# --------------------------------------------------

def compute_noise(gray):

    denoised = cv2.GaussianBlur(
        gray,
        (5, 5),
        0
    )

    noise = cv2.absdiff(
        gray,
        denoised
    )

    return float(np.std(noise))


# --------------------------------------------------
# White Ratio
# --------------------------------------------------

def compute_white_ratio(gray):

    return float(
        np.mean(gray > WHITE_THRESHOLD)
    )


# --------------------------------------------------
# Black Ratio
# --------------------------------------------------

def compute_black_ratio(gray):

    return float(
        np.mean(gray < BLACK_THRESHOLD)
    )


# --------------------------------------------------
# Edge Density
# --------------------------------------------------

def compute_edge_density(gray):

    edges = cv2.Canny(
        gray,
        100,
        200
    )

    return float(
        np.count_nonzero(edges)
        / edges.size
    )


# --------------------------------------------------
# Empty Detection
# --------------------------------------------------

def detect_empty(gray):

    variance = np.var(gray)

    return variance < 5


# --------------------------------------------------
# Background Detection
# --------------------------------------------------

def detect_background_only(

    white_ratio,
    black_ratio,
    edge_density

):

    if white_ratio > 0.98:
        return True

    if black_ratio > 0.98:
        return True

    if edge_density < 0.001:
        return True

    return False


# --------------------------------------------------
# Main Analyzer
# --------------------------------------------------

def analyze_quality(images):

    print("\n==============================")
    print("IMAGE QUALITY ANALYZER")
    print("==============================")

    for image in images:

        img = cv2.imread(image.path)

        if img is None:
            continue

        gray = cv2.cvtColor(
            img,
            cv2.COLOR_BGR2GRAY
        )

        image.blur_score = compute_blur(gray)

        image.noise_score = compute_noise(gray)

        image.white_ratio = compute_white_ratio(gray)

        image.black_ratio = compute_black_ratio(gray)

        image.edge_density = compute_edge_density(gray)

        image.is_empty = detect_empty(gray)

        image.background_only = detect_background_only(

            image.white_ratio,

            image.black_ratio,

            image.edge_density

        )

    print(f"Quality computed for {len(images)} images")

    print("\nSample Quality")

    for image in images[:5]:

        print(

            f"Page {image.page_no} | "

            f"Blur={image.blur_score:.1f} | "

            f"Noise={image.noise_score:.1f} | "

            f"Edges={image.edge_density:.3f} | "

            f"White={image.white_ratio:.2f} | "

            f"Empty={image.is_empty}"

        )

    return images