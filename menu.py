import tkinter as tk
from tkinter import messagebox
from game import GameBoard
from game import run_game


def configure_board_size():
    selected_size = board_size_var.get()
    selected_difficulty = difficulty_var.get()

    if selected_size in ["6", "8"]:
        run_game(board_size=int(selected_size), difficulty=selected_difficulty)


def show_menu():
    global board_size_var
    global difficulty_var
    global menu_window

    menu_window = tk.Tk()
    menu_window.title("Menú del Juego Reversi")

    label = tk.Label(menu_window, text="Bienvenido al juego Reversi", font=("Helvetica", 16))
    label.pack(pady=20)

    board_size_label = tk.Label(menu_window, text="Seleccione el tamaño del tablero:")
    board_size_label.pack()

    board_size_var = tk.StringVar()

    board_size_6 = tk.Radiobutton(menu_window, text="6x6", variable=board_size_var, value="6")
    board_size_6.pack()

    board_size_8 = tk.Radiobutton(menu_window, text="8x8", variable=board_size_var, value="8")
    board_size_8.pack()

    difficulty_label = tk.Label(menu_window, text="Seleccione la dificultad:")
    difficulty_label.pack()

    difficulty_var = tk.StringVar()

    easy_button = tk.Radiobutton(menu_window, text="Fácil", variable=difficulty_var, value="Fácil")
    easy_button.pack()

    medium_button = tk.Radiobutton(menu_window, text="Medio", variable=difficulty_var, value="Medio")
    medium_button.pack()

    hard_button = tk.Radiobutton(menu_window, text="Difícil", variable=difficulty_var, value="Difícil")
    hard_button.pack()

    configure_button = tk.Button(menu_window, text="Jugar", command=configure_board_size)
    configure_button.pack()

    exit_button = tk.Button(menu_window, text="Salir", command=menu_window.quit)
    exit_button.pack()

    menu_window.mainloop()


if __name__ == "__main__":
    show_menu()
