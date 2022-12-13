Один из архитектурных паттернов для разработки [[flutter|flutter-приложений]]. Базируется на [[#провайдер|провайдерах]] 




# Провайдер
это полиморфный объект, который инкапсулирует часть состояния какого-то другого объекта и позволяет "слушать" это состояние. 
* Заменяет [[singleton]], [[dipendancy injection|dp]] или [[inheritted widget]], позволяя обращаться к состоянию из разных частей программы
* включает в себя ряд оптимизаций, позволяющий обновлять только то, что было непосредственно затронуто изменением состояния инкапсулированного объекта
пример:
```dart 
final myProvider = Provider((ref) {  
	return MyValue();  
});
```
провайдеры должны быть всегда `final`. `Provider` - самая простая реализация провайдера. Также есть `StreamProvider`, `StateNotifierProvider` и прочие. В конструктор передается функция, которая создает общее состояние. Получает на вход объект `ref`, 

| Название                                                                                                                           | Инициализирующая функция             | Пример                                                               |
| ---------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------ | -------------------------------------------------------------------- |
| [Provider](https://riverpod.dev/docs/providers/provider)                                                                           | Returns any type                     | A service class / computed property (filtered list)                  |
| [StateProvider](https://riverpod.dev/docs/providers/state_provider)                                                                | Returns any type                     | A filter condition / simple state object                             |
| [FutureProvider](https://riverpod.dev/docs/providers/future_provider)                                                              | Returns a Future of any type         | A result from an API call                                            |
| [StreamProvider](https://riverpod.dev/docs/providers/stream_provider)                                                              | Returns a Stream of any type         | A stream of results from an API                                      |
| [StateNotifierProvider](https://riverpod.dev/docs/providers/state_notifier_provider)                                               | Returns a subclass of StateNotifier  | A complex state object that is immutable except through an interface |
| [ChangeNotifierProvider](https://pub.dev/documentation/flutter_riverpod/latest/flutter_riverpod/ChangeNotifierProvider-class.html) | Returns a subclass of ChangeNotifier | A complex state object that requires mutability                      |

Модификаторы провайдеров
У всех провайдеров есть встроенные способы добавить дополнительный функционал. 
```dart
	final myAutoDisposeProvider = StateProvider.autoDispose<int>((ref) => 0);
	final myFamilyProvider = Provider.family<String, int>((ref, id) => '$id');
```
на данный момент существуют два модификатора провайдера: 
1. .autoDispose - автоматически уничтожает состояние в случае, если его никто не "слушает"
2. .family - позволяет создавать провайдер с использованием внешних параметров
Можно использовать несколько модификаторов разом: 
```dart
final userProvider = FutureProvider.autoDispose.family<User, int>((ref, userId) async {
  return fetchUser(userId);
});
```
## чтение провайдера
```dart
class HomeView extends ConsumerStatefulWidget {
  const HomeView({Key? key}): super(key: key);

  @override
  HomeViewState createState() => HomeViewState();
}

class HomeViewState extends ConsumerState<HomeView> {
  @override
  void initState() {
    super.initState();
    // "ref" can be used in all life-cycles of a StatefulWidget.
    ref.read(counterProvider);
  }

  @override
  Widget build(BuildContext context) {
    // We can also use "ref" to listen to a provider inside the build method
    final counter = ref.watch(counterProvider);
    return Text('$counter');
  }
}
```

```jupyter
import matplotlib.pyplot as plt
plt.plot([i for i in range(10)], [1])
```
