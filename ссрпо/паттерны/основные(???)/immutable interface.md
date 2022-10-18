---
creation date: 2022-10-18 12:33
modification date: вторник 18-го октября 2022 12:33:43
---

Определяет интерфейс, в котором декларируются методы, не изменяющие его состояние
Пример:
```c++
class ImmutablePoint2D{
public:
	virtual ~ImmutablePoint2D() = default;
	virtual int getX() const = 0;
	virtual int getY() const = 0;
private:
	int _x, _y;
};

class Point2D : ImmutablePoint2D{
public: 
	Point2D(int x, int y): _x(x), _y(y) {}
	virtual int getX() const override {return _x;}
	virtual int getY() const override {return _y;}
	void setX(int x) {_x = x;}
	void setY(int y) {_y = y;} 
private: 
	int _x, _y;
}

int main() {
	ImmutablePoint2D * point = new Point2D(2,5);
	std::cout << point->getX() << " " << point->getY() << std::endl;
}
```

UML-диарамма будет выглядеть соответственно так:
```plantuml-ascii
interface ImmutablePoint2D
class Point2D
ImmutablePoint2D <|-- Point2D

interface ImmutablePoint2D{
	public virtual ~ImmutablePoint2D() = default;
	public virtual int getX() const = 0;
	public virtual int getY() const = 0;
	---
	private int _x
	private int _y
}

class Point2D{
	public Point2D(int x, int y): _x(x), _y(y) {}
	public virtual int getX() const override {return _x;}
	public virtual int getY() const override {return _y;}
	public void setX(int x) {_x = x;}
	public void setY(int y) {_y = y;} 
	---
	private int _x
	private int _y
}
```

### Особенности
Плюсы: 
* четко передает намерения о неизменяемости класса
Минусы
* для библиотечных классов необходимо предусматривать заранее

### Альтернативы
1. Immutable wrapper