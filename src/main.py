import tkrender
import os

if __name__ == "__main__":
    # Patching working directory
    main_path = os.path.realpath(__file__)
    main_dir = os.path.dirname(main_path)
    os.chdir(main_dir)

    # Running app
    app = tkrender.UI()
    app.mainloop()