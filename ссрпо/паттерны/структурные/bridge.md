---
creation date: 2022-04-11 04:07
modification date: вторник 18-го октября 2022 15:39:50
---

Необходим в тех случаях, когда нужно реализовать журналирование в различные места: файл, консоль, удаленный компьютер
для каждого варианта логгера нужны однопоточный и многопоточный варианты реализации
* Выделяется дополнительная иерархия, в которой реализовано представление изначальной иерархии
Мост также позволяет разделить абстракцию и реализацию так, чтобы они могли изменяться независимо друг от друга
uml-диаграмма моста
```plantuml
class Client
interface Abstraction{
operation()
}
class RefinedAbstraction
abstract class Implementor{
operatorImp()
}
class ConcreteImplementorA{
operatorImp()
}
class ConcreteImplementorB{
operatorImp()
}

Client --> Abstraction
Abstraction ->Implementor : implementor
RefinedAbstraction -|> Abstraction
ConcreteImplementorA --|> Implementor
ConcreteImplementorB --|> Implementor
```
плюсы: 
* упрощает модифицирование кода реализации
минусы: 
* усложняет реализацию
* ухудшает производительность

#важно  Мост и [[adapter|адаптер]] имеют схожую структуру, но цели их использования различны. Когда как адаптер применяют для адаптации уже существующих классов в систему, мост используется на стадии ее проектирования
