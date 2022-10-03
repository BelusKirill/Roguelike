import tcod

from actions import MovementAction, EscapeAction
from input_handlers import EventHandler


def main() -> None:
    screen_width = 80
    screen_height = 50

    player_x = int(screen_width / 2)
    player_y = int(screen_height / 2)

    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD #Делим изоброжение на плитки
    )

    event_handler = EventHandler()

    #Создаем терминал с параметрами
    with tcod.context.new_terminal( 
        screen_width,
        screen_height,
        tileset=tileset,
        title="Roguelike terminal",
        vsync=True,
    ) as context:
        root_console = tcod.Console(screen_width, screen_height, order="F")
        while True:
            root_console.print(x=player_x, y=player_y, string="@")

            context.present(root_console) #Обновление консоли

            root_console.clear()
         
            for event in tcod.event.wait(): #Отслеживает ивенты
                action = event_handler.dispatch(event)

                if action is None:
                    continue

                if isinstance(action, MovementAction):
                    player_x += action.dx
                    player_y += action.dy

                elif isinstance(action, EscapeAction):
                    raise SystemExit()


if __name__ == "__main__":
    main()