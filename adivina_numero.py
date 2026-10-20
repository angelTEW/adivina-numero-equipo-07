import random
from datetime import datetime


GAME_TITLE = "Adivina el número"
DIFFICULTIES = {
    "1": {"name": "Fácil", "minimum": 1, "maximum": 20, "attempts": 8},
    "2": {"name": "Medio", "minimum": 1, "maximum": 50, "attempts": 7},
    "3": {"name": "Difícil", "minimum": 1, "maximum": 100, "attempts": 6},
}


def get_player_name():
    name = input("¿Cómo te llamas? ").strip()
    if not name:
        return "Jugador"
    return name


def choose_difficulty():
    print("\nSelecciona una dificultad:")
    print("1. Fácil (1–20, 8 intentos)")
    print("2. Medio (1–50, 7 intentos)")
    print("3. Difícil (1–100, 6 intentos)")

    while True:
        choice = input("Opción: ").strip().lower()
        if choice in DIFFICULTIES:
            return DIFFICULTIES[choice]
        print("Opción inválida. Por favor elige 1, 2 o 3.")


def read_valid_guess(minimum, maximum):
    """Pide un número y repite la pregunta hasta que sea válido, sin gastar intentos."""
    while True:
        raw_guess = input(f"Escribe un número entre {minimum} y {maximum}: ").strip()

        # Evita que el programa truene con texto vacío o letras
        try:
            guess = int(raw_guess)
        except ValueError:
            print("Entrada inválida. Debe ser un número entero.")
            continue

        # Verifica que esté dentro del rango
        if guess < minimum or guess > maximum:
            print(f"El número debe estar entre {minimum} y {maximum}.")
            continue

        return guess


def calculate_score(attempts_used, maximum_attempts, won):
    if not won:
        return 0

    points = (maximum_attempts - attempts_used) * 10
    if points < 0:
        points = 0
    return points


def play_round(settings):
    secret_number = random.randint(settings["minimum"], settings["maximum"])
    attempts_used = 0
    won = False

    print(
        f"\nAdivina el número entre {settings['minimum']} y "
        f"{settings['maximum']}. Tienes {settings['attempts']} intentos."
    )

    # Ahora sí respeta exactamente el número de intentos anunciado (< en lugar de <=)
    while attempts_used < settings["attempts"] and not won:
        guess = read_valid_guess(settings["minimum"], settings["maximum"])
        attempts_used += 1

        if guess < secret_number:
            print("Muy bajo.")
        elif guess > secret_number:
            print("Muy alto.")
        else:
            print("¡Correcto!")
            won = True

        # Informa cuántos intentos le quedan si no ha ganado
        if not won and attempts_used < settings["attempts"]:
            remaining = settings["attempts"] - attempts_used
            print(f"Te quedan {remaining} intentos.")

    if won:
        print(f"Adivinaste en {attempts_used} intentos.")
    else:
        print(f"Se acabaron los intentos. El número era {secret_number}.")

    score = calculate_score(attempts_used, settings["attempts"], won)
    return {
        "won": won,
        "attempts": attempts_used,
        "score": score,
        "secret_number": secret_number,
    }


def save_score(scores, player_name, result, difficulty_name):
    record = {
        "name": player_name,
        "score": result["score"],
        "won": result["won"],
        "difficulty": difficulty_name,
        "played_at": datetime.now(),
    }
    scores.append(record)
    scores.sort(key=lambda item: item["score"], reverse=True)
    return record


def show_leaderboard(scores):
    print("\n--- Mejores resultados de esta sesión ---")
    if len(scores) == 0:
        print("Todavía no hay resultados.")
        return

    for position, result in enumerate(scores[:3], start=1):
        print(
            f"{position}. {result['name']} — {result['score']} puntos "
            f"({result['difficulty']})"
        )


def play_game(scores):
    player_name = get_player_name()
    settings = choose_difficulty()
    result = play_round(settings)
    save_score(scores, player_name, result, settings["name"])
    show_leaderboard(scores)


def ask_to_play_again():
    """Tolera espacios, mayúsculas, minúsculas y acentos."""
    answer = input("\n¿Quieres jugar otra vez? (s/n): ").strip().lower()
    return answer in ["s", "si", "sí", "yes", "y"]


def main():
    print(f"=== {GAME_TITLE} ===")
    print("Adivina el número secreto y consigue la mayor puntuación.")
    scores = []

    while True:
        play_game(scores)
        if not ask_to_play_again():
            break

    print("\nGracias por jugar")


if __name__ == "__main__":
    main()
