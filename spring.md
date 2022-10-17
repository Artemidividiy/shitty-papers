### Возможные ошибки

если все выглядит нормально при запуске как на скрине ниже
![[Pasted image 20220423002024.png]]
необходимо установить модуль *spring-boot-starter-web*, закинув его в подобие pubspec.yaml, который здесь называется pom.xml и является частью maven (см ниже)
`
<dependency>  
    <groupId>org.springframework.boot</groupId>  
    <artifactId>spring-boot-starter-web</artifactId>  
</dependency>
`

---

### Про контроллеры

чтобы добавить контроллер, нужно
1. создать новый класс <Name>Controller
2. импортировать 
	<org.springframework.web.bind.annotation.RestController>
3.добавить аннотацию <@RestController>
4. прописываем методы контроллера
5. докидываем на методы аннотацию <@RequestMapping("<adress>")>

### Про тестирование

---

Access key ID: dF0RSPTIbCLlRq3cTF1VKw

Access key secret: jl2OWssAPwyLXXkSeeB_ofT94C1wdB6Vi7lRU0-fduDZsDooamnEJl1tHPMwED-wYb8P_h-1_lPWrkEFbnHTrw