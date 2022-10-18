---
creation date: 2022-04-11 04:04
modification date: вторник 18-го октября 2022 14:21:15

---

---
Абстрактная фабрика - порождающий паттерн проектирования, решающий проблему создания семейства [[связанные классы|связных объектов]], не привязываясь к конкретным классам объектов[^1]. Класс, который представляет собой интерфейс для создания компонентов системы[^2].


### Обозначение проблемы

Допустим, нам необходимо создать симмулятор мебельного магазина. У нас есть семейство связанных классов

Также абстрактную фабрику имеет смысл применять в случае, если в программе уже используется [[factory method |фабричный метод]]. 

---
Плюсы: 
* изолирует конкретные классы 
* упрощает замену семейств продуктов
* гарантирует сочитаемость продуктов
Минусы: 
* сложно добавить поддержку нового вида продуктов
Ограничения: 
* Система не должна зависеть от того, как создаются, компонуются и представляются входящие в нее объекты
* Входящие в семейство взаимосвязанные объекты *должны использоваться вместе*, и  необходимо обеспечить выполнение этого ограничения
* Система должна конфигурироваться одним из семейств составляющих ее объектов 
* Требуется предоставить библиотеку объектов, раскрывая только их интерфейсы, но не реализацию

Паттерн реализуется созданием абстрактного класса Factory, который представляет собой интерфейс для создания компонентов системы (например, для оконного интерфейса он может создавать окна и кнопки). Далее строятся классы, реализующие этот абстрактный класс
```
interface Button is
    method paint()

// Семейства продуктов имеют те же вариации (macOS/Windows).
class WinButton implements Button is
    method paint() is
        // Отрисовать кнопку в стиле Windows.

class MacButton implements Button is
    method paint() is
        // Отрисовать кнопку в стиле macOS.

interface Checkbox is
    method paint()

class WinCheckbox implements Checkbox is
    method paint() is
        // Отрисовать чекбокс в стиле Windows.

class MacCheckbox implements Checkbox is
    method paint() is
        // Отрисовать чекбокс в стиле macOS.

// Абстрактная фабрика знает обо всех абстрактных типах
// продуктов.
interface GUIFactory is
    method createButton():Button
    method createCheckbox():Checkbox

// Каждая конкретная фабрика знает и создаёт только продукты
// своей вариации.
class WinFactory implements GUIFactory is
    method createButton():Button is
        return new WinButton()
    method createCheckbox():Checkbox is
        return new WinCheckbox()

// Несмотря на то, что фабрики оперируют конкретными классами,
// их методы возвращают абстрактные типы продуктов. Благодаря
// этому фабрики можно взаимозаменять, не изменяя клиентский
// код.
class MacFactory implements GUIFactory is
    method createButton():Button is
        return new MacButton()
    method createCheckbox():Checkbox is
        return new MacCheckbox()

// Для кода, использующего фабрику, не важно, с какой конкретно
// фабрикой он работает. Все получатели продуктов работают с
// ними через общие интерфейсы.
class Application is
    private field factory: GUIFactory
    private field button: Button
    constructor Application(factory: GUIFactory) is
        this.factory = factory
    method createUI()
        this.button = factory.createButton()
    method paint()
        button.paint()

// Приложение выбирает тип конкретной фабрики и создаёт её
// динамически, исходя из конфигурации или окружения.
class ApplicationConfigurator is
    method main() is
        config = readApplicationConfigFile()

        if (config.OS == "Windows") then
            factory = new WinFactory()
        else if (config.OS == "Mac") then
            factory = new MacFactory()
        else
            throw new Exception("Error! Unknown operating system.")

        Application app = new Application(factory)
```

UML-диаграмма абстрактной фабрики будет иметь вид: 
```plantuml
Button <|-- WinButton : реализует интерфейс
Button <|-- MacButton : реализует интерфейс
Checkbox <|-- WinCheckbox : реализует интерфейс
Checkbox <|-- MacCheckbox : реализует интерфейс
GUIFactory <|-- WinFactory : реализует интерфейс
GUIFactory <|-- MacFactory : реализует интерфейс
Application -- GUIFactory : Поле класса
Application -- Button : Поле класса
ApplicationConfigurator -- Application : Поле класса
GUIFactory -- Checkbox : Поле класса
GUIFactory -- Button : Поле класса
interface Button {
	paint()
}
class MacButton {
	paint()
}
class WinButton {
	paint()
}

interface Checkbox{
	paint()
}
class  MacCheckbox{
	paint()
}
class  WinCheckbox{
	paint()
}

interface GUIFactory {
	Button createButton()
	Checkbox createCheckbox()
}
class WinFactory {
	Button createButton()
	Checkbox createCheckbox()
}
class MacFactory{
	Button createButton()
	Checkbox createCheckbox()
}
class Application {
- GUIFactory factory
- Button button
Application(GUIFactory factory)
createUI()
paint() => button.paint()
}

class ApplicationConfigurator{
	main()
}
```
## Источники

[^1]: [рефакторинг гуру::абстрактная фабрика](https://refactoring.guru/ru/design-patterns/abstract-factory)
[^2]: лекция 2