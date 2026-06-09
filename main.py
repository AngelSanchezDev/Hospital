import os
import sys

# se agrega la raíz del proyecto al path para poder importar módulos internos sin errores.
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from views.login import LoginView


def iniciar_app():
    # se crea y ejecuta la ventana principal de acceso del sistema.
    app = LoginView()
    app.mainloop()


if __name__ == "__main__":
    iniciar_app()
