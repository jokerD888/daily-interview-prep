SEED_CARDS = []

# Java基础 (20张)
java_cards = [
    ("Java中==和equals的区别是什么？", "==比较的是对象引用地址，equals()默认比较引用地址，但String等类重写了equals()方法用于比较内容是否相同。"),
    ("String、StringBuilder、StringBuffer的区别？", "String是不可变类，每次修改生成新对象；StringBuilder可变，线程不安全，性能高；StringBuffer可变，线程安全(synchronized)，性能略低。"),
    ("Java的四种引用类型是什么？", "强引用(Strong)：GC不会回收；软引用(Soft)：内存不足时回收；弱引用(Weak)：下次GC必定回收；虚引用(Phantom)：用于跟踪对象回收状态。"),
    ("HashMap的底层实现原理？", "JDK1.8后：数组+链表+红黑树。通过hash计算数组下标，冲突用链地址法，链表长度≥8且数组≥64时转红黑树。put()时key的hashCode经扰动函数处理后取模。"),
    ("什么是线程安全的HashMap替代方案？", "ConcurrentHashMap：JDK1.7分段锁(Segment)，JDK1.8 CAS+synchronized锁链表/红黑树头节点。Hashtable：全表锁，已淘汰。Collections.synchronizedMap()：包装器方式。"),
    ("ArrayList和LinkedList的区别？", "ArrayList底层是数组，随机访问O(1)，增删O(n)；LinkedList底层是双向链表，随机访问O(n)，增删O(1)。内存上ArrayList更紧凑。"),
    ("try-catch-finally中return的执行顺序？", "先执行try中return的表达式(计算值)，再执行finally，最后返回。如果finally中有return，会覆盖try中的return。System.exit(0)可阻止finally执行。"),
    ("什么是Java的反射机制？", "反射允许运行时获取类的完整结构(字段、方法、构造器)并动态调用。通过Class.forName()或.class获取Class对象。常用于框架(IoC容器)、动态代理。"),
    ("JVM内存模型包括哪些区域？", "堆(Heap)：存放对象实例，GC主要区域；方法区(Metaspace)：类信息、常量、静态变量；虚拟机栈：栈帧存储局部变量、操作数栈；本地方法栈；程序计数器。"),
    ("什么是类加载机制？双亲委派模型？", "加载→验证→准备→解析→初始化。双亲委派：类加载器先委托父加载器查找，父无法加载时子类才加载。保证核心类安全性，防止重复加载。"),
    ("volatile关键字的作用？", "保证变量的可见性(修改立即刷新到主内存)和禁止指令重排序(内存屏障)。不保证原子性。适用场景：状态标记、DCL双重检查锁定单例。"),
    ("synchronized和Lock的区别？", "synchronized是JVM内置关键字，自动释放锁，非公平锁；Lock(java.util.concurrent.locks)是API级，需手动unlock()，支持公平锁、可中断、超时获取、多条件变量。"),
    ("Java中有哪些方式创建线程？", "1.继承Thread类；2.实现Runnable接口；3.实现Callable接口(有返回值和异常)；4.线程池(ExecutorService)。推荐使用线程池，避免频繁创建销毁。"),
    ("什么是线程池？核心参数有哪些？", "线程池复用线程，控制并发数。ThreadPoolExecutor核心参数：corePoolSize核心线程数、maximumPoolSize最大线程数、keepAliveTime空闲存活时间、workQueue工作队列、RejectedExecutionHandler拒绝策略。"),
    ("Java异常体系是怎样的？", "Throwable为根，分Error(系统级，不可处理)和Exception。Exception分RuntimeException(非受检，如NPE)和受检异常(如IOException，必须catch或throws)。"),
    ("什么是泛型？类型擦除是什么？", "泛型提供编译时类型安全检查。Java泛型通过类型擦除实现：编译后泛型信息被擦除，替换为上限类型(Object)。桥方法用于保持多态性。"),
    ("深拷贝和浅拷贝的区别？", "浅拷贝：基本类型复制值，引用类型复制引用地址(共享对象)。深拷贝：引用类型也递归创建新对象。实现方式：实现Cloneable+重写clone()或序列化反序列化。"),
    ("final、finally、finalize的区别？", "final修饰类不可继承、方法不可重写、变量不可修改；finally是try-catch的必执行块；finalize是Object的方法，GC回收前调用(已废弃，JDK9标记deprecated)。"),
    ("什么是Java动态代理？", "运行时动态创建代理类。JDK动态代理：基于接口，Proxy.newProxyInstance()；CGLIB动态代理：基于继承(字节码)，不需接口。Spring AOP默认JDK动态代理，无接口时用CGLIB。"),
    ("Java中的SPI机制是什么？", "Service Provider Interface，服务提供者接口。通过在META-INF/services下配置实现类全限定名，ServiceLoader动态加载。用于可插拔设计，如JDBC驱动加载。"),
]
for q, a in java_cards:
    SEED_CARDS.append({"question": q, "answer": a, "importance_score": 5, "category": "Java基础"})

# Spring (20张)
spring_cards = [
    ("Spring IoC容器原理是什么？", "IoC(Inversion of Control)控制反转，由Spring容器管理Bean的创建和依赖注入。核心是BeanFactory和ApplicationContext。通过反射+XML/注解配置创建对象并注入依赖。"),
    ("Spring Bean的生命周期？", "实例化→属性赋值→BeanNameAware→BeanFactoryAware→ApplicationContextAware→BeanPostProcessor前置处理→InitializingBean→init-method→BeanPostProcessor后置处理→使用→DisposableBean→destroy-method。"),
    ("Spring AOP的实现原理？", "AOP面向切面编程，Spring AOP基于动态代理：有接口用JDK动态代理，无接口用CGLIB。AspectJ是编译时织入。核心概念：切面(Aspect)、连接点(JoinPoint)、通知(Advice)、切点(Pointcut)。"),
    ("Spring事务传播行为有哪些？", "REQUIRED(默认，有则加入无则新建)、SUPPORTS(有则加入无则非事务)、MANDATORY(必须有事务)、REQUIRES_NEW(挂起当前新建独立事务)、NOT_SUPPORTED(非事务执行)、NEVER(不允许事务)、NESTED(嵌套事务)。"),
    ("@Autowired和@Resource的区别？", "@Autowired是Spring注解，默认按类型注入，配合@Qualifier按名称；@Resource是JSR-250注解，默认按名称注入，找不到再按类型。"),
    ("Spring Boot自动配置原理？", "@SpringBootApplication包含@EnableAutoConfiguration，通过@Import导入AutoConfigurationImportSelector，扫描META-INF/spring.factories中的自动配置类，结合@Conditional条件注解决定是否生效。"),
    ("Spring MVC处理请求的流程？", "DispatcherServlet接收请求→HandlerMapping匹配Controller→HandlerAdapter执行Controller→返回ModelAndView→ViewResolver解析视图→渲染返回。前后端分离时@RestController直接返回JSON。"),
    ("Spring中用到了哪些设计模式？", "单例(Bean默认单例)、工厂(BeanFactory)、代理(AOP)、模板(JdbcTemplate)、观察者(ApplicationEvent)、适配器(HandlerAdapter)、策略(Resource)、装饰器。"),
    ("@Transactional失效的场景有哪些？", "1.非public方法；2.自调用(同类方法调用不走代理)；3.异常被catch未抛出；4.rollbackFor设置不正确；5.数据库引擎不支持事务(MyISAM)；6.多线程环境。"),
    ("什么是Spring循环依赖？如何解决？", "A依赖B，B依赖A。Spring通过三级缓存解决构造器注入外的循环依赖：singletonObjects(完全初始化)、earlySingletonObjects(提前暴露)、singletonFactories(对象工厂)。构造器注入无法解决，需用@Lazy。"),
    ("Spring Boot Starter是什么？", "一组依赖描述符，将相关依赖打包，简化Maven/Gradle配置。如spring-boot-starter-web自动引入spring-webmvc、tomcat、jackson等。命名规范：官方spring-boot-starter-xxx，第三方xxx-spring-boot-starter。"),
    ("Spring Bean的作用域有哪些？", "singleton(默认，单例)、prototype(每次获取新建)、request(一次请求)、session(一次会话)、application(ServletContext生命周期)、websocket。"),
    ("Spring如何处理线程安全问题？", "Bean默认单例无状态，不存可变数据；有状态Bean用prototype作用域；或用ThreadLocal隔离线程数据。Controller/Dao/Service无状态天然线程安全。"),
    ("@Configuration和@Component的区别？", "@Configuration标注的类会被CGLIB代理，内部@Bean方法调用会从容器获取同一个实例(保证单例)；@Component内部@Bean方法是普通方法调用，每次new新对象。"),
    ("Spring事件监听机制？", "基于观察者模式：ApplicationEvent(事件)、ApplicationListener(监听器)、ApplicationEventPublisher(发布者)。@EventListener注解简化。异步事件用@Async配合。"),
    ("Spring Boot如何实现热部署？", "spring-boot-devtools：检测classpath变化自动重启(通过双ClassLoader实现快速重启)。JRebel(商业工具，不做重启，直接替换字节码)。IDEA开启自动编译+Build Project Automatically。"),
    ("Spring Security的认证流程？", "请求经过SecurityFilterChain过滤器链→AuthenticationFilter提取用户名密码→封装为AuthenticationToken→AuthenticationManager调用AuthenticationProvider验证→UserDetailsService加载用户→验证通过返回Authenticated Authentication→存入SecurityContextHolder。"),
    ("Spring Boot配置文件加载优先级？", "命令行参数>JVM属性>操作系统环境变量>application-{profile}.yml>application.yml。bootstrap.yml(Spring Cloud)优先级更高。配置中心>本地配置。"),
    ("Spring Boot Actuator是什么？", "生产级监控端点：/health健康检查、/info应用信息、/metrics指标(内存、线程、HTTP请求)、/env环境变量、/loggers日志级别动态调整、/mappings接口映射。需注意安全暴露。"),
    ("@ComponentScan的作用？", "组件扫描注解，指定Spring扫描Bean的包路径。默认扫描当前类所在包及子包。可自定义basePackages、includeFilters(Custom Filter)、excludeFilters排除。"),
]
for q, a in spring_cards:
    SEED_CARDS.append({"question": q, "answer": a, "importance_score": 5, "category": "Spring"})

# 操作系统 (20张)
os_cards = [
    ("进程和线程的区别？", "进程是资源分配基本单位，线程是CPU调度基本单位。进程间内存隔离，线程共享进程内存。进程创建销毁开销大，线程轻量。一个进程至少有一个线程。"),
    ("进程间通信(IPC)有哪些方式？", "管道(pipe/fifo，半双工)、消息队列、共享内存(最快)、信号量(同步)、信号、Socket(跨网络)。共享内存最快但需配合信号量同步。"),
    ("死锁的四个必要条件？如何预防？", "互斥、持有并等待、不可剥夺、循环等待。预防：破坏任一条件——资源一次性分配、可剥夺资源、资源有序分配(按编号顺序申请)。银行家算法避免死锁。"),
    ("什么是虚拟内存？", "将磁盘作为内存扩展，程序使用虚拟地址，MMU映射到物理内存或磁盘页面。按需调页：缺页中断→加载所需页面→若内存满则页面置换。地址空间分离，进程安全隔离。"),
    ("页面置换算法有哪些？", "FIFO(先进先出，Belady异常)、LRU(最近最久未使用)、LFU(最少使用)、OPT(最佳置换，理论最优不可实现)、Clock(时钟算法，近似LRU)。Linux使用改进的LRU。"),
    ("用户态和内核态的区别？如何切换？", "用户态只能访问受限资源，内核态可访问全部。切换：系统调用(int 0x80/syscall指令)、异常(缺页)、外设中断。切换会保存上下文，开销较大。"),
    ("什么是上下文切换？", "CPU从执行一个进程/线程切换到另一个，保存当前上下文(寄存器、PC)到PCB，加载下一个进程上下文。线程切换比进程切换开销小(不需切换地址空间)。频繁切换影响性能。"),
    ("堆和栈的区别？", "栈：编译器自动管理，存放局部变量、函数参数，LIFO，速度快，空间有限。堆：程序员手动管理(malloc/free)，存放动态分配对象，速度慢，空间大，可能内存碎片。"),
    ("什么是内存对齐？为什么需要？", "CPU读取内存按字长对齐访问，未对齐数据需两次读取。编译器自动对齐，空间换时间。struct中字段排列影响大小。#pragma pack可设置对齐系数。"),
    ("select、poll、epoll的区别？", "select：fd_set位图，1024限制，O(n)轮询；poll：pollfd数组，无数量限制，O(n)；epoll(Linux)：红黑树+就绪链表，O(1)，支持ET/LT模式。epoll是Linux下高性能I/O多路复用首选。"),
    ("硬链接和软链接的区别？", "硬链接：同一inode多个文件名，删除最后一个才释放，不能跨文件系统，不能链接目录；软链接(符号链接)：独立inode存路径字符串，可跨文件系统，源删除后失效。"),
    ("什么是缓冲区溢出？", "向缓冲区写入超过其容量的数据，覆盖相邻内存。栈溢出可覆盖返回地址，劫持程序，执行恶意代码。防护：ASLR地址随机化、Stack Canary栈金丝雀、DEP数据执行保护。"),
    ("并发和并行的区别？", "并发：逻辑上同时执行，单核CPU时间片轮转；并行：物理上同时执行，多核CPU同时运行。多线程是并发手段，在多核上可并行。"),
    ("什么是CAS？ABA问题？", "CAS(Compare And Swap)：比较值和预期值相等则更新，原子操作。ABA：值被改为B又改回A，CAS检测不出。解决：加版本号(AtomicStampedReference)或时间戳。"),
    ("Linux文件权限模型？", "rwx(read/write/execute)三组：所有者、所属组、其他用户。数字表示：r=4,w=2,x=1。chmod 755=rwxr-xr-x。特殊权限SUID(4)、SGID(2)、粘滞位(1)。"),
    ("什么是自旋锁？", "线程循环等待锁释放(忙等待)，不释放CPU。适合锁持有时间极短的场景，避免上下文切换开销。CAS是实现基础。长时间自旋浪费CPU。Linux内核广泛使用。"),
    ("操作系统如何管理内存？", "分段(逻辑分段，如代码段/数据段)→分页(固定大小页框，页表映射)→段页式(先分段再分页)。MMU硬件完成虚拟地址→物理地址转换。TLB缓存页表项加速转换。"),
    ("什么是中断和异常？", "中断：外设异步信号(键盘输入、网卡数据)，可屏蔽。异常：CPU执行指令时同步产生(除零、缺页、断点)，不可屏蔽。中断处理：保存现场→执行ISR→恢复现场。"),
    ("进程有哪些状态？", "新建→就绪(Ready)→运行(Running)→阻塞(Blocked/等待I/O)→终止(Terminated)。就绪↔运行由调度器切换，运行→阻塞等待事件，阻塞→就绪事件发生。挂起态(Suspend)增加外存换出。"),
    ("什么是零拷贝？", "减少内核空间和用户空间数据拷贝次数。传统read+write：DMA→内核缓冲区→用户缓冲区→Socket缓冲区。sendfile/mmap：DMA→内核缓冲区→Socket缓冲区(省去用户态拷贝)。Kafka、Nginx大量使用。"),
]
for q, a in os_cards:
    SEED_CARDS.append({"question": q, "answer": a, "importance_score": 5, "category": "操作系统"})
