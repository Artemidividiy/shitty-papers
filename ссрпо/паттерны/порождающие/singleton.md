---
creation date: 2022-04-11 04:05
modification date: вторник 18-го октября 2022 15:39:43
---

> Порождающий шаблон проектирования, гарантирующий, что в однопроцессном приложении будет единственный экземпляр некоторого класса, и предоставляющий глобальную точку доступа к этому экземпляру
> (с) лекции

Решает задачу, когда необходимо гарантировать, что код работает с глобальным объектом 

singleton полезен, когда: 
1. должен быть ровно один экземпляр некоторого класса, легко доступного для всех клиентов
2. единственный экземпляр должен расширяться путем пораждения подклассов, и клиентам нужно иметь возможность работать с расширенным экземпляром без модификации своего кода 
плюсы: 
* контролируемый доступ к единственному экземпляру
минусы: 
* глобальные объекты могут быть вредны для объектного программирования, в некоторых случаях приводит к созданию немасштабируемого проекта
* усложняет написание модульных тестов и следствие TDD

```c++
class OnlyOne{
public: 
	static OnlyOne& init(){
		static OnlyOne theSingleInstance;
		return the SingleInstance;
	}
private: 
	OnlyOne(){}
	OnlyOne(const OnlyOne& root) = delete;
	OnlyOne& operator =(const OnlyOne&) = delete;
};
```
