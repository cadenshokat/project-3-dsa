import pygame
from typing import Dict

from main import ALGORITHMS, DATASETS, load_dataset, time_algorithm
from generator.generate import (
    generate_random_large_range,
    sort_dataset_file,
    generate_reverse_sorted_dataset,
    generate_almost_sorted_dataset,
)

WIDTH, HEIGHT = 1100, 700
BG_COLOR = (18, 18, 24)
PANEL_COLOR = (30, 32, 40)
CARD_COLOR = (40, 44, 55)
CARD_HIGHLIGHT = (70, 80, 110)
BAR_COLOR = (120, 200, 255)
BAR_OUTLINE = (200, 220, 255)
TEXT_COLOR = (235, 235, 245)
SUCCESS_COLOR = (80, 220, 120)
MUTED_TEXT = (170, 170, 185)
ACCENT_COLOR = (255, 170, 90)
BUTTON_COLOR = (70, 80, 110)
BUTTON_HOVER = (100, 120, 160)
BUTTON_DISABLED = (60, 60, 70)

AXIS_COLOR = (120, 125, 135)

class Button:
    def __init__(self, rect: pygame.Rect, label: str, font, callback=None):
        self.rect = rect
        self.label = label
        self.font = font
        self.callback = callback
        self.enabled = True

    def draw(self, surface, mouse_pos):
        hovered = self.rect.collidepoint(mouse_pos) and self.enabled
        color = BUTTON_HOVER if hovered else BUTTON_COLOR
        if not self.enabled:
            color = BUTTON_DISABLED

        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        text_surf = self.font.render(self.label, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def handle_event(self, event, mouse_pos):
        if not self.enabled:
            return
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(mouse_pos):
                if self.callback:
                    self.callback()


def draw_text(surface, text, x, y, font, color=TEXT_COLOR, center=False):
    img = font.render(text, True, color)
    rect = img.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    surface.blit(img, rect)


def regenerate_all_datasets(max_val: int):
    print(f"Regenerating datasets (random max = {max_val})...")
    random_path = generate_random_large_range(seed=None, max_val=max_val)
    print(f"  Random: {random_path}")

    sorted_path = sort_dataset_file()
    print(f"  Sorted: {sorted_path}")

    reversed_path = generate_reverse_sorted_dataset()
    print(f"  Reversed: {reversed_path}")

    almost_sorted_path = generate_almost_sorted_dataset(seed=None)
    print(f"  Almost sorted: {almost_sorted_path}")


def run_benchmarks_for_algorithm(algo_key: str) -> Dict[str, float]:
    algo_info = ALGORITHMS[algo_key]
    algo_fn = algo_info["fn"]

    results: Dict[str, float] = {}
    for ds_key, ds_info in DATASETS.items():
        nums = load_dataset(ds_info["filename"])
        print(f"Running {algo_info['name']} on {ds_info['name']}...")
        _, time_ms = time_algorithm(algo_fn, nums)
        results[ds_key] = time_ms

    return results


def draw_top_bar(screen, algo_buttons, selected_algo_key, mouse_pos, title_font, small_font):
    pygame.draw.rect(screen, PANEL_COLOR, pygame.Rect(0, 0, WIDTH, 90))

    draw_text(screen, "Sorting Algorithm Demo", 30, 20, title_font)
    draw_text(
        screen,
        "Select an algorithm, then compare its performance across datasets.",
        30,
        50,
        small_font,
        color=MUTED_TEXT,
    )

    for key, button in algo_buttons.items():
        button.draw(screen, mouse_pos)

    if selected_algo_key in algo_buttons:
        rect = algo_buttons[selected_algo_key].rect
        pygame.draw.line(
            screen,
            ACCENT_COLOR,
            (rect.x, rect.bottom + 3),
            (rect.right, rect.bottom + 3),
            3,
        )


def draw_dataset_panel(screen, dataset_results: Dict[str, float], medium_font, small_font):
    panel_rect = pygame.Rect(WIDTH - 320, 90, 320, HEIGHT - 90)
    pygame.draw.rect(screen, PANEL_COLOR, panel_rect)

    margin = 16
    x = panel_rect.x + margin
    y = panel_rect.y + margin

    draw_text(screen, "Datasets", x, y, medium_font)
    y += 30
    draw_text(screen, "Each bar in the chart represents", x, y, small_font, color=MUTED_TEXT)
    y += 20
    draw_text(screen, "the time for this algorithm on", x, y, small_font, color=MUTED_TEXT)
    y += 20
    draw_text(screen, "each dataset.", x, y, small_font, color=MUTED_TEXT)
    y += 30

    card_height = 90
    gap = 12

    for key, info in DATASETS.items():
        rect = pygame.Rect(x, y, panel_rect.width - 2 * margin, card_height)
        pygame.draw.rect(screen, CARD_COLOR, rect, border_radius=10)

        draw_text(screen, info["name"], rect.x + 10, rect.y + 8, small_font)

        desc = info["description"]
        draw_text(screen, desc, rect.x + 10, rect.y + 30, small_font, color=MUTED_TEXT)

        if dataset_results and key in dataset_results:
            t_ms = dataset_results[key]
            time_str = f"{t_ms:.1f} ms"
            draw_text(
                screen,
                time_str,
                rect.right - 180,
                rect.bottom - 25,
                small_font,
                color=ACCENT_COLOR,
                center=False,
            )
        else:
            draw_text(
                screen,
                "Not run yet",
                rect.right - 180,
                rect.bottom - 25,
                small_font,
                color=(130, 130, 140),
                center=False,
            )

        y += card_height + gap


def draw_bar_chart(
    screen,
    selected_algo_key,
    dataset_results: Dict[str, float],
    chart_rect: pygame.Rect,
    large_font,
    small_font,
    datasets_regenerated: bool,
):
    pygame.draw.rect(screen, PANEL_COLOR, chart_rect, border_radius=10)

    inner_margin = 40
    x0 = chart_rect.x + inner_margin
    x1 = chart_rect.right - inner_margin
    y0 = chart_rect.y + inner_margin + 20
    y1 = chart_rect.bottom - inner_margin

    if selected_algo_key is None:
        if datasets_regenerated:
            draw_text(
                screen,
                "Datasets regenerated!",
                chart_rect.centerx,
                (y0 + y1) / 2,
                small_font,
                color=SUCCESS_COLOR,
                center=True,
            )
        else:
            draw_text(
                screen,
                "Pick an algorithm above to run benchmarks.",
                chart_rect.centerx,
                chart_rect.y + 20,
                small_font,
                color=MUTED_TEXT,
                center=True,
            )
        return
    else:
        algo_name = ALGORITHMS[selected_algo_key]["name"]
        draw_text(
            screen,
            f"Runtime on Datasets ({algo_name})",
            chart_rect.centerx,
            chart_rect.y + 18,
            small_font,
            center=True,
        )

    if not dataset_results:
        if datasets_regenerated:
            draw_text(
                screen,
                "Datasets regenerated!",
                chart_rect.centerx,
                (y0 + y1) / 2,
                small_font,
                color=SUCCESS_COLOR,
                center=True,
            )
        else:
            draw_text(
                screen,
                "Press an algorithm button to run.",
                chart_rect.centerx,
                (y0 + y1) / 2,
                small_font,
                color=MUTED_TEXT,
                center=True,
            )
        return

    pygame.draw.line(screen, AXIS_COLOR, (x0, y0), (x0, y1), 2)
    pygame.draw.line(screen, AXIS_COLOR, (x0, y1), (x1, y1), 2)

    ds_keys = list(DATASETS.keys())
    times = [dataset_results[k] for k in ds_keys if k in dataset_results]
    if not times:
        return

    max_time = max(times)
    if max_time <= 0:
        max_time = 1.0

    chart_width = x1 - x0
    chart_height = y1 - y0

    n = len(ds_keys)
    bar_width = chart_width / (n * 1.5)
    gap = bar_width / 2

    for i, ds_key in enumerate(ds_keys):
        ds_info = DATASETS[ds_key]
        t_ms = dataset_results.get(ds_key, 0.0)

        height_ratio = t_ms / max_time if max_time > 0 else 0
        bar_h = height_ratio * chart_height

        cx = x0 + gap + i * (bar_width + gap)
        x = cx - bar_width / 2
        y = y1 - bar_h

        rect = pygame.Rect(x, y, bar_width, bar_h)
        pygame.draw.rect(screen, BAR_COLOR, rect, border_radius=4)
        pygame.draw.rect(screen, BAR_OUTLINE, rect, width=1, border_radius=4)

        label = ds_info["name"]
        draw_text(screen, label, cx, y1 + 8, small_font, color=MUTED_TEXT, center=True)

        label_time = f"{t_ms:.0f} ms"
        draw_text(screen, label_time, cx, y - 18, small_font, color=ACCENT_COLOR, center=True)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sorting Algorithm Visualization Demo")

    title_font = pygame.font.SysFont("segoeui", 28, bold=True)
    medium_font = pygame.font.SysFont("segoeui", 22, bold=True)
    small_font = pygame.font.SysFont("segoeui", 16)

    clock = pygame.time.Clock()

    max_random_value = 1000
    datasets_regenerated = False

    regenerate_all_datasets(max_random_value)

    selected_algo_key = None
    dataset_results: Dict[str, float] = {}

    algo_buttons: Dict[str, Button] = {}
    btn_width = 170
    btn_height = 40
    spacing = 10
    total_width = len(ALGORITHMS) * (btn_width + spacing) - spacing
    start_x = WIDTH - total_width - 30
    y_top = 20

    for i, (key, info) in enumerate(sorted(ALGORITHMS.items(), key=lambda kv: kv[0])):
        x = start_x + i * (btn_width + spacing)
        rect = pygame.Rect(x, y_top, btn_width, btn_height)

        def make_callback(k=key):
            def callback():
                nonlocal selected_algo_key, dataset_results
                selected_algo_key = k
                dataset_results = run_benchmarks_for_algorithm(k)
            return callback

        algo_buttons[key] = Button(rect, info["name"], small_font, callback=make_callback())

    regen_rect = pygame.Rect(30, HEIGHT - 60, 220, 40)
    regen_button = Button(regen_rect, "Regenerate Datasets", small_font)

    max_value_box_rect = pygame.Rect(regen_rect.right + 230, regen_rect.y, 80, regen_rect.height)
    max_dec_rect = pygame.Rect(max_value_box_rect.x - 40, regen_rect.y, 30, regen_rect.height)
    max_inc_rect = pygame.Rect(max_value_box_rect.right + 10, regen_rect.y, 30, regen_rect.height)

    def regen_callback():
        nonlocal dataset_results, selected_algo_key, datasets_regenerated
        regenerate_all_datasets(max_random_value)
        dataset_results = {}
        selected_algo_key = None
        datasets_regenerated = True

    regen_button.callback = regen_callback

    def dec_max_callback():
        nonlocal max_random_value
        if max_random_value > 10:
            max_random_value = max(10, max_random_value - 1000)
            print(f"Random max decreased to {max_random_value}")

    def inc_max_callback():
        nonlocal max_random_value
        if max_random_value < 1_000_000:
            max_random_value = min(1_000_000, max_random_value + 1000)
            print(f"Random max increased to {max_random_value}")

    max_dec_button = Button(max_dec_rect, "-", small_font, callback=dec_max_callback)
    max_inc_button = Button(max_inc_rect, "+", small_font, callback=inc_max_callback)

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

            for button in algo_buttons.values():
                button.handle_event(event, mouse_pos)
            regen_button.handle_event(event, mouse_pos)
            max_dec_button.handle_event(event, mouse_pos)
            max_inc_button.handle_event(event, mouse_pos)

        screen.fill(BG_COLOR)

        draw_top_bar(screen, algo_buttons, selected_algo_key, mouse_pos, title_font, small_font)

        chart_rect = pygame.Rect(30, 110, WIDTH - 380, HEIGHT - 180)
        draw_bar_chart(screen, selected_algo_key, dataset_results, chart_rect, medium_font, small_font, datasets_regenerated)

        draw_dataset_panel(screen, dataset_results, medium_font, small_font)

        regen_button.draw(screen, mouse_pos)
        label_x = regen_rect.right + 40
        label_y = regen_rect.y + 10
        draw_text(screen, "Dataset Max Value:", label_x, label_y, small_font, color=MUTED_TEXT)

        pygame.draw.rect(screen, CARD_COLOR, max_value_box_rect, border_radius=8)
        value_str = str(max_random_value)
        value_surf = small_font.render(value_str, True, TEXT_COLOR)
        value_rect = value_surf.get_rect(center=max_value_box_rect.center)
        screen.blit(value_surf, value_rect)

        max_dec_button.draw(screen, mouse_pos)
        max_inc_button.draw(screen, mouse_pos)

        esc_text = "ESC to quit"
        esc_surf = small_font.render(esc_text, True, MUTED_TEXT)
        esc_rect = esc_surf.get_rect()
        esc_rect.bottom = regen_rect.bottom
        esc_rect.right = WIDTH - 40
        screen.blit(esc_surf, esc_rect)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
