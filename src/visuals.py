import pygame
from main import ALGORITHMS, DATASETS, load_dataset, time_algorithm

WIDTH, HEIGHT = 900, 600
BG_COLOR = (30, 30, 30)
BAR_COLOR = (100, 180, 255)
TEXT_COLOR = (230, 230, 230)
AXIS_COLOR = (200, 200, 200)

def run_benchmarks_for_dataset(dataset_key: str) -> dict[str, float]:
    dataset_info = DATASETS[dataset_key]
    numbers = load_dataset(dataset_info["filename"])

    results: dict[str, float] = {}

    for key, algo in ALGORITHMS.items():
        name = algo["name"]
        print(f"Running {name} on {dataset_info['name']}...")
        _, time_ms = time_algorithm(algo["fn"], numbers)
        results[name] = time_ms

    return results


def draw_text(surface, text, x, y, font, color=TEXT_COLOR, center=False):
    img = font.render(text, True, color)
    rect = img.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    surface.blit(img, rect)


def draw_bar_chart(screen, results: dict[str, float], dataset_name: str, font, small_font):
    screen.fill(BG_COLOR)

    draw_text(
        screen,
        f"Dataset: {dataset_name}",
        WIDTH // 2,
        30,
        font,
        center=True,
    )

    if not results:
        draw_text(
            screen,
            "Press 1–4 to run benchmarks for a dataset.",
            WIDTH // 2,
            HEIGHT // 2,
            small_font,
            center=True,
        )
        pygame.display.flip()
        return

    algo_names = list(results.keys())
    times = [results[name] for name in algo_names]

    max_time = max(times) if times else 1.0

    chart_top = 100
    chart_bottom = HEIGHT - 120
    chart_height = chart_bottom - chart_top
    chart_left = 80
    chart_right = WIDTH - 80
    chart_width = chart_right - chart_left

    # Axes
    pygame.draw.line(screen, AXIS_COLOR, (chart_left, chart_top), (chart_left, chart_bottom), 2)
    pygame.draw.line(screen, AXIS_COLOR, (chart_left, chart_bottom), (chart_right, chart_bottom), 2)

    n = len(algo_names)
    if n == 0:
        pygame.display.flip()
        return

    bar_width = chart_width / (n * 1.5)
    gap = bar_width / 2

    for i, name in enumerate(algo_names):
        time_ms = results[name]

        height_ratio = time_ms / max_time if max_time > 0 else 0
        bar_height = height_ratio * chart_height

        x = chart_left + gap + i * (bar_width + gap)
        y = chart_bottom - bar_height

        rect = pygame.Rect(x, y, bar_width, bar_height)
        pygame.draw.rect(screen, BAR_COLOR, rect)

        label = name.split()[0]
        draw_text(screen, label, x, chart_bottom + 5, small_font)

        time_label = f"{time_ms:.0f} ms"
        draw_text(screen, time_label, x, y - 20, small_font)

    y_instr = HEIGHT - 60
    draw_text(
        screen,
        "Press 1: Random | 2: Sorted | 3: Reverse | 4: Almost Sorted | ESC: Quit",
        WIDTH // 2,
        y_instr,
        small_font,
        center=True,
    )

    pygame.display.flip()


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sorting Algorithm Visualization (Timing Bar Chart)")

    font = pygame.font.SysFont("arial", 28)
    small_font = pygame.font.SysFont("arial", 20)

    clock = pygame.time.Clock()

    current_dataset_key = None
    current_results: dict[str, float] = {}

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                elif event.key == pygame.K_1 and "1" in DATASETS:
                    current_dataset_key = "1"
                    current_results = run_benchmarks_for_dataset("1")
                elif event.key == pygame.K_2 and "2" in DATASETS:
                    current_dataset_key = "2"
                    current_results = run_benchmarks_for_dataset("2")
                elif event.key == pygame.K_3 and "3" in DATASETS:
                    current_dataset_key = "3"
                    current_results = run_benchmarks_for_dataset("3")
                elif event.key == pygame.K_4 and "4" in DATASETS:
                    current_dataset_key = "4"
                    current_results = run_benchmarks_for_dataset("4")

        dataset_name = DATASETS[current_dataset_key]["name"] if current_dataset_key else "None"
        draw_bar_chart(screen, current_results, dataset_name, font, small_font)

        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()
