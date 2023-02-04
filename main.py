from dependency_injector.wiring import Provide, inject

from src.contaners import Container
from src.use_case import UseCase


@inject
def main(use_case: UseCase = Provide[Container.use_case]) -> None:
    use_case.run()


if __name__ == "__main__":
    container = Container()
    container.init_resources()
    container.wire(modules=[__name__])
    main()
