
---
creation date: 2022-10-18 11:04
modification date: вторник 18-го октября 2022 11:28:53
---

> Объект внешне выражает некоторое поведение, но в реальности передаёт ответственность за выполнение этого поведения связанному объекту.
> (c) лекции

## реализация
реализуем данный шаблон на языке c++
```c++
class I {
	public: 
		virtual void f() = 0;
		virtual void g() = 0;
};

class A : I {
	public void f() {std::cout << "А: вызывается метод f()" << std::endl;}
	public void g() {std::cout << "А: вызывается метод g()" << std::endl;}
};

class B : I {
	public void f() {std::cout << "B: вызывается метод f()" << std::endl;}
	public void g() {std::cout << "B: вызывается метод g()" << std::endl;}
};
```
На диаграмме это выглядит так 
```plantuml-ascii

class I
class A
class B
I <|--- A
I <|--- B

class I {
	virtual void f()
	virtual void g()
}

class A {
	public void f()
	public void g()
}

class B {
	public void f()
	public void g()
}
```

```c++
class C: I{
private:
	I *m_i;
public:
	C() : m_i(new A()) {}
	virtual ~C(){
		delete m_i;
	}
	void f() {m_i->f();}
	void g() {m_i->g();}
	void toA() {
		delete m_i;
		m_i = new A();
	}
	void toB() {
		delete m_i;
		m_i = new A();
	}
};
```
```c++
int main() {
	C c;
	c.f();
	c.g();
	c.toB();
	c.f();
	c.g();
	return 0;
}
```
Суть этого кода в том, что при работе метода `main()` будут работать сначала методы, реализованные в `A`, но после работы метода `toB()` при повторном вызове методов класса c уже будет реализация методов класса `B`

#важно Стоит отметить, что шаблон делелегирования является фундаментальной абстракцией на основе которой реализованы другие шаблоны
