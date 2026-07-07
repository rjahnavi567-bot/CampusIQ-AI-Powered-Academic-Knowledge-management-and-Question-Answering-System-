from app.services.image_v2.sliding_window_detector import detect_window_figures

window_figures = detect_window_figures(page_image)

print(window_figures[:5])