# Test Report

## Conclusion

PASS

## Fallback Used

True

## Checks

### mvn clean compile

status: PASS
returncode: 0

stdout:

[WARNING] 
[WARNING] Some problems were encountered while building the effective settings
[WARNING] Unrecognised tag: 'repository' (position: START_TAG seen ...</activation>\n      <repository>... @70:19)  @ D:\soft\apache-maven-3.9.9\conf\settings.xml, line 70, column 19
[WARNING] 
[INFO] Scanning for projects...
[INFO] 
[INFO] -------------------< com.example:library-management >-------------------
[INFO] Building library-management 0.0.1-SNAPSHOT
[INFO]   from pom.xml
[INFO] --------------------------------[ jar ]---------------------------------
[INFO] 
[INFO] --- clean:3.2.0:clean (default-clean) @ library-management ---
[INFO] Deleting D:\work\project\Pipeline\heavenly-reations\target
[INFO] 
[INFO] --- resources:3.2.0:resources (default-resources) @ library-management ---
[INFO] Using 'UTF-8' encoding to copy filtered resources.
[INFO] Using 'UTF-8' encoding to copy filtered properties files.
[INFO] Copying 2 resources
[INFO] Copying 0 resource
[INFO] 
[INFO] --- compiler:3.10.1:compile (default-compile) @ library-management ---
[INFO] Changes detected - recompiling the module!
[INFO] Compiling 12 source files to D:\work\project\Pipeline\heavenly-reations\target\classes
[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] ------------------------------------------------------------------------
[INFO] Total time:  1.155 s
[INFO] Finished at: 2026-05-28T01:07:05+08:00
[INFO] ------------------------------------------------------------------------


stderr:

(empty)

### mvn test

status: PASS
returncode: 0

stdout:

isbn4_0_0_, book0_.title as title5_0_0_ from books book0_ where book0_.id=?
Hibernate: update books set author=?, inventory_count=?, isbn=?, title=? where id=?
[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 3.578 s - in com.example.library.controller.BookControllerIntegrationTest
[INFO] Running com.example.library.LibraryApplicationTests
2026-05-28 01:07:12.180  INFO 28176 --- [           main] .b.t.c.SpringBootTestContextBootstrapper : Neither @ContextConfiguration nor @ContextHierarchy found for test class [com.example.library.LibraryApplicationTests], using SpringBootContextLoader
2026-05-28 01:07:12.181  INFO 28176 --- [           main] o.s.t.c.support.AbstractContextLoader    : Could not detect default resource locations for test class [com.example.library.LibraryApplicationTests]: no resource found for suffixes {-context.xml, Context.groovy}.
2026-05-28 01:07:12.181  INFO 28176 --- [           main] t.c.s.AnnotationConfigContextLoaderUtils : Could not detect default configuration classes for test class [com.example.library.LibraryApplicationTests]: LibraryApplicationTests does not declare any static, non-private, non-final, nested classes annotated with @Configuration.
2026-05-28 01:07:12.183  INFO 28176 --- [           main] .b.t.c.SpringBootTestContextBootstrapper : Found @SpringBootConfiguration com.example.library.LibraryApplication for test class com.example.library.LibraryApplicationTests
2026-05-28 01:07:12.184  INFO 28176 --- [           main] .b.t.c.SpringBootTestContextBootstrapper : Loaded default TestExecutionListener class names from location [META-INF/spring.factories]: [org.springframework.boot.test.mock.mockito.MockitoTestExecutionListener, org.springframework.boot.test.mock.mockito.ResetMocksTestExecutionListener, org.springframework.boot.test.autoconfigure.restdocs.RestDocsTestExecutionListener, org.springframework.boot.test.autoconfigure.web.client.MockRestServiceServerResetTestExecutionListener, org.springframework.boot.test.autoconfigure.web.servlet.MockMvcPrintOnlyOnFailureTestExecutionListener, org.springframework.boot.test.autoconfigure.web.servlet.WebDriverTestExecutionListener, org.springframework.boot.test.autoconfigure.webservices.client.MockWebServiceServerTestExecutionListener, org.springframework.test.context.web.ServletTestExecutionListener, org.springframework.test.context.support.DirtiesContextBeforeModesTestExecutionListener, org.springframework.test.context.event.ApplicationEventsTestExecutionListener, org.springframework.test.context.support.DependencyInjectionTestExecutionListener, org.springframework.test.context.support.DirtiesContextTestExecutionListener, org.springframework.test.context.transaction.TransactionalTestExecutionListener, org.springframework.test.context.jdbc.SqlScriptsTestExecutionListener, org.springframework.test.context.event.EventPublishingTestExecutionListener]
2026-05-28 01:07:12.184  INFO 28176 --- [           main] .b.t.c.SpringBootTestContextBootstrapper : Using TestExecutionListeners: [org.springframework.test.context.web.ServletTestExecutionListener@e79c25, org.springframework.test.context.support.DirtiesContextBeforeModesTestExecutionListener@ce1cd3, org.springframework.test.context.event.ApplicationEventsTestExecutionListener@46a125, org.springframework.boot.test.mock.mockito.MockitoTestExecutionListener@31989d, org.springframework.boot.test.autoconfigure.SpringBootDependencyInjectionTestExecutionListener@8f310a, org.springframework.test.context.support.DirtiesContextTestExecutionListener@7d914c, org.springframework.test.context.transaction.TransactionalTestExecutionListener@15940af, org.springframework.test.context.jdbc.SqlScriptsTestExecutionListener@1f8df69, org.springframework.test.context.event.EventPublishingTestExecutionListener@e6a9bd, org.springframework.boot.test.mock.mockito.ResetMocksTestExecutionListener@47bc9c, org.springframework.boot.test.autoconfigure.restdocs.RestDocsTestExecutionListener@100c143, org.springframework.boot.test.autoconfigure.web.client.MockRestServiceServerResetTestExecutionListener@404f9d, org.springframework.boot.test.autoconfigure.web.servlet.MockMvcPrintOnlyOnFailureTestExecutionListener@142b729, org.springframework.boot.test.autoconfigure.web.servlet.WebDriverTestExecutionListener@164f81, org.springframework.boot.test.autoconfigure.webservices.client.MockWebServiceServerTestExecutionListener@1cb8599]

  .   ____          _            __ _ _
 /\\ / ___'_ __ _ _(_)_ __  __ _ \ \ \ \
( ( )\___ | '_ | '_| | '_ \/ _` | \ \ \ \
 \\/  ___)| |_)| | | | | || (_| |  ) ) ) )
  '  |____| .__|_| |_|_| |_\__, | / / / /
 =========|_|==============|___/=/_/_/_/
 :: Spring Boot ::               (v2.7.18)

2026-05-28 01:07:12.202  INFO 28176 --- [           main] c.e.library.LibraryApplicationTests      : Starting LibraryApplicationTests using Java 1.8.0_291 on DESKTOP-UTKLBD2 with PID 28176 (started by Administrator in D:\work\project\Pipeline\heavenly-reations)
2026-05-28 01:07:12.203  INFO 28176 --- [           main] c.e.library.LibraryApplicationTests      : The following 1 profile is active: "test"
2026-05-28 01:07:12.295  INFO 28176 --- [           main] .s.d.r.c.RepositoryConfigurationDelegate : Bootstrapping Spring Data JPA repositories in DEFAULT mode.
2026-05-28 01:07:12.303  INFO 28176 --- [           main] .s.d.r.c.RepositoryConfigurationDelegate : Finished Spring Data repository scanning in 7 ms. Found 2 JPA repository interfaces.
2026-05-28 01:07:12.376  INFO 28176 --- [           main] o.hibernate.jpa.internal.util.LogHelper  : HHH000204: Processing PersistenceUnitInfo [name: default]
2026-05-28 01:07:12.379  INFO 28176 --- [           main] com.zaxxer.hikari.HikariDataSource       : HikariPool-2 - Starting...
2026-05-28 01:07:12.380  INFO 28176 --- [           main] com.zaxxer.hikari.HikariDataSource       : HikariPool-2 - Start completed.
2026-05-28 01:07:12.380  INFO 28176 --- [           main] org.hibernate.dialect.Dialect            : HHH000400: Using dialect: org.hibernate.dialect.H2Dialect
Hibernate: drop table if exists books CASCADE 
Hibernate: drop table if exists borrowed_books CASCADE 
Hibernate: create table books (id bigint generated by default as identity, author varchar(255), inventory_count integer not null check (inventory_count>=0), isbn varchar(255) not null, title varchar(255), primary key (id))
Hibernate: create table borrowed_books (id bigint generated by default as identity, borrowed_date timestamp not null, returned_date timestamp, book_id bigint not null, primary key (id))
Hibernate: alter table books add constraint UK_kibbepcitr0a3cpk3rfr7nihn unique (isbn)
Hibernate: alter table borrowed_books add constraint FKirp80rty69v7va8179fdkbrls foreign key (book_id) references books
2026-05-28 01:07:12.404  INFO 28176 --- [           main] o.h.e.t.j.p.i.JtaPlatformInitiator       : HHH000490: Using JtaPlatform implementation: [org.hibernate.engine.transaction.jta.platform.internal.NoJtaPlatform]
2026-05-28 01:07:12.404  INFO 28176 --- [           main] j.LocalContainerEntityManagerFactoryBean : Initialized JPA EntityManagerFactory for persistence unit 'default'
2026-05-28 01:07:12.516  WARN 28176 --- [           main] JpaBaseConfiguration$JpaWebConfiguration : spring.jpa.open-in-view is enabled by default. Therefore, database queries may be performed during view rendering. Explicitly configure spring.jpa.open-in-view to disable this warning
2026-05-28 01:07:12.700  INFO 28176 --- [           main] c.e.library.LibraryApplicationTests      : Started LibraryApplicationTests in 0.515 seconds (JVM running for 4.463)
[INFO] Tests run: 1, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.503 s - in com.example.library.LibraryApplicationTests
[INFO] Running com.example.library.service.BookServiceTest
[INFO] Tests run: 6, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.166 s - in com.example.library.service.BookServiceTest
[INFO] Running com.example.library.service.BorrowServiceTest
[INFO] Tests run: 3, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.034 s - in com.example.library.service.BorrowServiceTest
2026-05-28 01:07:12.913  INFO 28176 --- [ionShutdownHook] j.LocalContainerEntityManagerFactoryBean : Closing JPA EntityManagerFactory for persistence unit 'default'
2026-05-28 01:07:12.913  INFO 28176 --- [ionShutdownHook] .SchemaDropperImpl$DelayedDropActionImpl : HHH000477: Starting delayed evictData of schema as part of SessionFactory shut-down'
Hibernate: drop table if exists books CASCADE 
Hibernate: drop table if exists borrowed_books CASCADE 
2026-05-28 01:07:13.128  INFO 28176 --- [ionShutdownHook] com.zaxxer.hikari.HikariDataSource       : HikariPool-1 - Shutdown initiated...
2026-05-28 01:07:13.134  INFO 28176 --- [ionShutdownHook] com.zaxxer.hikari.HikariDataSource       : HikariPool-1 - Shutdown completed.
2026-05-28 01:07:13.135  INFO 28176 --- [ionShutdownHook] j.LocalContainerEntityManagerFactoryBean : Closing JPA EntityManagerFactory for persistence unit 'default'
2026-05-28 01:07:13.135  INFO 28176 --- [ionShutdownHook] .SchemaDropperImpl$DelayedDropActionImpl : HHH000477: Starting delayed evictData of schema as part of SessionFactory shut-down'
Hibernate: drop table if exists books CASCADE 
Hibernate: drop table if exists borrowed_books CASCADE 
2026-05-28 01:07:13.137  INFO 28176 --- [ionShutdownHook] com.zaxxer.hikari.HikariDataSource       : HikariPool-2 - Shutdown initiated...
2026-05-28 01:07:13.137  INFO 28176 --- [ionShutdownHook] com.zaxxer.hikari.HikariDataSource       : HikariPool-2 - Shutdown completed.
[INFO] 
[INFO] Results:
[INFO] 
[INFO] Tests run: 14, Failures: 0, Errors: 0, Skipped: 0
[INFO] 
[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] ------------------------------------------------------------------------
[INFO] Total time:  7.125 s
[INFO] Finished at: 2026-05-28T01:07:13+08:00
[INFO] ------------------------------------------------------------------------


stderr:

(empty)

### mvn clean package

status: PASS
returncode: 0

stdout:

m.example.library.LibraryApplicationTests
2026-05-28 01:07:20.511  INFO 25256 --- [           main] .b.t.c.SpringBootTestContextBootstrapper : Neither @ContextConfiguration nor @ContextHierarchy found for test class [com.example.library.LibraryApplicationTests], using SpringBootContextLoader
2026-05-28 01:07:20.511  INFO 25256 --- [           main] o.s.t.c.support.AbstractContextLoader    : Could not detect default resource locations for test class [com.example.library.LibraryApplicationTests]: no resource found for suffixes {-context.xml, Context.groovy}.
2026-05-28 01:07:20.511  INFO 25256 --- [           main] t.c.s.AnnotationConfigContextLoaderUtils : Could not detect default configuration classes for test class [com.example.library.LibraryApplicationTests]: LibraryApplicationTests does not declare any static, non-private, non-final, nested classes annotated with @Configuration.
2026-05-28 01:07:20.514  INFO 25256 --- [           main] .b.t.c.SpringBootTestContextBootstrapper : Found @SpringBootConfiguration com.example.library.LibraryApplication for test class com.example.library.LibraryApplicationTests
2026-05-28 01:07:20.514  INFO 25256 --- [           main] .b.t.c.SpringBootTestContextBootstrapper : Loaded default TestExecutionListener class names from location [META-INF/spring.factories]: [org.springframework.boot.test.mock.mockito.MockitoTestExecutionListener, org.springframework.boot.test.mock.mockito.ResetMocksTestExecutionListener, org.springframework.boot.test.autoconfigure.restdocs.RestDocsTestExecutionListener, org.springframework.boot.test.autoconfigure.web.client.MockRestServiceServerResetTestExecutionListener, org.springframework.boot.test.autoconfigure.web.servlet.MockMvcPrintOnlyOnFailureTestExecutionListener, org.springframework.boot.test.autoconfigure.web.servlet.WebDriverTestExecutionListener, org.springframework.boot.test.autoconfigure.webservices.client.MockWebServiceServerTestExecutionListener, org.springframework.test.context.web.ServletTestExecutionListener, org.springframework.test.context.support.DirtiesContextBeforeModesTestExecutionListener, org.springframework.test.context.event.ApplicationEventsTestExecutionListener, org.springframework.test.context.support.DependencyInjectionTestExecutionListener, org.springframework.test.context.support.DirtiesContextTestExecutionListener, org.springframework.test.context.transaction.TransactionalTestExecutionListener, org.springframework.test.context.jdbc.SqlScriptsTestExecutionListener, org.springframework.test.context.event.EventPublishingTestExecutionListener]
2026-05-28 01:07:20.514  INFO 25256 --- [           main] .b.t.c.SpringBootTestContextBootstrapper : Using TestExecutionListeners: [org.springframework.test.context.web.ServletTestExecutionListener@1f8df69, org.springframework.test.context.support.DirtiesContextBeforeModesTestExecutionListener@e6a9bd, org.springframework.test.context.event.ApplicationEventsTestExecutionListener@47bc9c, org.springframework.boot.test.mock.mockito.MockitoTestExecutionListener@100c143, org.springframework.boot.test.autoconfigure.SpringBootDependencyInjectionTestExecutionListener@404f9d, org.springframework.test.context.support.DirtiesContextTestExecutionListener@142b729, org.springframework.test.context.transaction.TransactionalTestExecutionListener@164f81, org.springframework.test.context.jdbc.SqlScriptsTestExecutionListener@1cb8599, org.springframework.test.context.event.EventPublishingTestExecutionListener@1671dda, org.springframework.boot.test.mock.mockito.ResetMocksTestExecutionListener@1b20860, org.springframework.boot.test.autoconfigure.restdocs.RestDocsTestExecutionListener@1a63110, org.springframework.boot.test.autoconfigure.web.client.MockRestServiceServerResetTestExecutionListener@680b0, org.springframework.boot.test.autoconfigure.web.servlet.MockMvcPrintOnlyOnFailureTestExecutionListener@13cd727, org.springframework.boot.test.autoconfigure.web.servlet.WebDriverTestExecutionListener@f82ba8, org.springframework.boot.test.autoconfigure.webservices.client.MockWebServiceServerTestExecutionListener@3cb756]

  .   ____          _            __ _ _
 /\\ / ___'_ __ _ _(_)_ __  __ _ \ \ \ \
( ( )\___ | '_ | '_| | '_ \/ _` | \ \ \ \
 \\/  ___)| |_)| | | | | || (_| |  ) ) ) )
  '  |____| .__|_| |_|_| |_\__, | / / / /
 =========|_|==============|___/=/_/_/_/
 :: Spring Boot ::               (v2.7.18)

2026-05-28 01:07:20.533  INFO 25256 --- [           main] c.e.library.LibraryApplicationTests      : Starting LibraryApplicationTests using Java 1.8.0_291 on DESKTOP-UTKLBD2 with PID 25256 (started by Administrator in D:\work\project\Pipeline\heavenly-reations)
2026-05-28 01:07:20.533  INFO 25256 --- [           main] c.e.library.LibraryApplicationTests      : The following 1 profile is active: "test"
2026-05-28 01:07:20.627  INFO 25256 --- [           main] .s.d.r.c.RepositoryConfigurationDelegate : Bootstrapping Spring Data JPA repositories in DEFAULT mode.
2026-05-28 01:07:20.633  INFO 25256 --- [           main] .s.d.r.c.RepositoryConfigurationDelegate : Finished Spring Data repository scanning in 6 ms. Found 2 JPA repository interfaces.
2026-05-28 01:07:20.743  INFO 25256 --- [           main] o.hibernate.jpa.internal.util.LogHelper  : HHH000204: Processing PersistenceUnitInfo [name: default]
2026-05-28 01:07:20.745  INFO 25256 --- [           main] com.zaxxer.hikari.HikariDataSource       : HikariPool-2 - Starting...
2026-05-28 01:07:20.745  INFO 25256 --- [           main] com.zaxxer.hikari.HikariDataSource       : HikariPool-2 - Start completed.
2026-05-28 01:07:20.745  INFO 25256 --- [           main] org.hibernate.dialect.Dialect            : HHH000400: Using dialect: org.hibernate.dialect.H2Dialect
Hibernate: drop table if exists books CASCADE 
Hibernate: drop table if exists borrowed_books CASCADE 
Hibernate: create table books (id bigint generated by default as identity, author varchar(255), inventory_count integer not null check (inventory_count>=0), isbn varchar(255) not null, title varchar(255), primary key (id))
Hibernate: create table borrowed_books (id bigint generated by default as identity, borrowed_date timestamp not null, returned_date timestamp, book_id bigint not null, primary key (id))
Hibernate: alter table books add constraint UK_kibbepcitr0a3cpk3rfr7nihn unique (isbn)
Hibernate: alter table borrowed_books add constraint FKirp80rty69v7va8179fdkbrls foreign key (book_id) references books
2026-05-28 01:07:20.765  INFO 25256 --- [           main] o.h.e.t.j.p.i.JtaPlatformInitiator       : HHH000490: Using JtaPlatform implementation: [org.hibernate.engine.transaction.jta.platform.internal.NoJtaPlatform]
2026-05-28 01:07:20.766  INFO 25256 --- [           main] j.LocalContainerEntityManagerFactoryBean : Initialized JPA EntityManagerFactory for persistence unit 'default'
2026-05-28 01:07:20.876  WARN 25256 --- [           main] JpaBaseConfiguration$JpaWebConfiguration : spring.jpa.open-in-view is enabled by default. Therefore, database queries may be performed during view rendering. Explicitly configure spring.jpa.open-in-view to disable this warning
2026-05-28 01:07:21.066  INFO 25256 --- [           main] c.e.library.LibraryApplicationTests      : Started LibraryApplicationTests in 0.55 seconds (JVM running for 4.408)
[INFO] Tests run: 1, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.539 s - in com.example.library.LibraryApplicationTests
[INFO] Running com.example.library.service.BookServiceTest
[INFO] Tests run: 6, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.149 s - in com.example.library.service.BookServiceTest
[INFO] Running com.example.library.service.BorrowServiceTest
[INFO] Tests run: 3, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.038 s - in com.example.library.service.BorrowServiceTest
2026-05-28 01:07:21.267  INFO 25256 --- [ionShutdownHook] j.LocalContainerEntityManagerFactoryBean : Closing JPA EntityManagerFactory for persistence unit 'default'
2026-05-28 01:07:21.267  INFO 25256 --- [ionShutdownHook] .SchemaDropperImpl$DelayedDropActionImpl : HHH000477: Starting delayed evictData of schema as part of SessionFactory shut-down'
Hibernate: drop table if exists books CASCADE 
Hibernate: drop table if exists borrowed_books CASCADE 
2026-05-28 01:07:21.474  INFO 25256 --- [ionShutdownHook] com.zaxxer.hikari.HikariDataSource       : HikariPool-1 - Shutdown initiated...
2026-05-28 01:07:21.475  INFO 25256 --- [ionShutdownHook] com.zaxxer.hikari.HikariDataSource       : HikariPool-1 - Shutdown completed.
2026-05-28 01:07:21.477  INFO 25256 --- [ionShutdownHook] j.LocalContainerEntityManagerFactoryBean : Closing JPA EntityManagerFactory for persistence unit 'default'
2026-05-28 01:07:21.477  INFO 25256 --- [ionShutdownHook] .SchemaDropperImpl$DelayedDropActionImpl : HHH000477: Starting delayed evictData of schema as part of SessionFactory shut-down'
Hibernate: drop table if exists books CASCADE 
Hibernate: drop table if exists borrowed_books CASCADE 
2026-05-28 01:07:21.479  INFO 25256 --- [ionShutdownHook] com.zaxxer.hikari.HikariDataSource       : HikariPool-2 - Shutdown initiated...
2026-05-28 01:07:21.480  INFO 25256 --- [ionShutdownHook] com.zaxxer.hikari.HikariDataSource       : HikariPool-2 - Shutdown completed.
[INFO] 
[INFO] Results:
[INFO] 
[INFO] Tests run: 14, Failures: 0, Errors: 0, Skipped: 0
[INFO] 
[INFO] 
[INFO] --- jar:3.2.2:jar (default-jar) @ library-management ---
[INFO] Building jar: D:\work\project\Pipeline\heavenly-reations\target\library-management-0.0.1-SNAPSHOT.jar
[INFO] 
[INFO] --- spring-boot:2.7.18:repackage (repackage) @ library-management ---
[INFO] Replacing main artifact with repackaged archive
[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] ------------------------------------------------------------------------
[INFO] Total time:  8.150 s
[INFO] Finished at: 2026-05-28T01:07:22+08:00
[INFO] ------------------------------------------------------------------------


stderr:

(empty)

### check target/*.jar

status: PASS
returncode: None

stdout:

D:\work\project\Pipeline\heavenly-reations\target\library-management-0.0.1-SNAPSHOT.jar

stderr:

(empty)

### java -jar D:\work\project\Pipeline\heavenly-reations\target\library-management-0.0.1-SNAPSHOT.jar

status: PASS
returncode: None

stdout:

nnectionAccess.obtainConnection(JdbcEnvironmentInitiator.java:181) ~[hibernate-core-5.6.15.Final.jar!/:5.6.15.Final]
	at org.hibernate.engine.jdbc.env.internal.JdbcEnvironmentInitiator.initiateService(JdbcEnvironmentInitiator.java:68) [hibernate-core-5.6.15.Final.jar!/:5.6.15.Final]
	at org.hibernate.engine.jdbc.env.internal.JdbcEnvironmentInitiator.initiateService(JdbcEnvironmentInitiator.java:35) [hibernate-core-5.6.15.Final.jar!/:5.6.15.Final]
	at org.hibernate.boot.registry.internal.StandardServiceRegistryImpl.initiateService(StandardServiceRegistryImpl.java:101) [hibernate-core-5.6.15.Final.jar!/:5.6.15.Final]
	at org.hibernate.service.internal.AbstractServiceRegistryImpl.createService(AbstractServiceRegistryImpl.java:272) [hibernate-core-5.6.15.Final.jar!/:5.6.15.Final]
	at org.hibernate.service.internal.AbstractServiceRegistryImpl.initializeService(AbstractServiceRegistryImpl.java:246) [hibernate-core-5.6.15.Final.jar!/:5.6.15.Final]
	at org.hibernate.service.internal.AbstractServiceRegistryImpl.getService(AbstractServiceRegistryImpl.java:223) [hibernate-core-5.6.15.Final.jar!/:5.6.15.Final]
	at org.hibernate.id.factory.internal.DefaultIdentifierGeneratorFactory.injectServices(DefaultIdentifierGeneratorFactory.java:175) [hibernate-core-5.6.15.Final.jar!/:5.6.15.Final]
	at org.hibernate.service.internal.AbstractServiceRegistryImpl.injectDependencies(AbstractServiceRegistryImpl.java:295) [hibernate-core-5.6.15.Final.jar!/:5.6.15.Final]
	at org.hibernate.service.internal.AbstractServiceRegistryImpl.initializeService(AbstractServiceRegistryImpl.java:252) [hibernate-core-5.6.15.Final.jar!/:5.6.15.Final]
	at org.hibernate.service.internal.AbstractServiceRegistryImpl.getService(AbstractServiceRegistryImpl.java:223) [hibernate-core-5.6.15.Final.jar!/:5.6.15.Final]
	at org.hibernate.boot.internal.InFlightMetadataCollectorImpl.<init>(InFlightMetadataCollectorImpl.java:173) [hibernate-core-5.6.15.Final.jar!/:5.6.15.Final]
	at org.hibernate.boot.model.process.spi.MetadataBuildingProcess.complete(MetadataBuildingProcess.java:127) [hibernate-core-5.6.15.Final.jar!/:5.6.15.Final]
	at org.hibernate.jpa.boot.internal.EntityManagerFactoryBuilderImpl.metadata(EntityManagerFactoryBuilderImpl.java:1460) [hibernate-core-5.6.15.Final.jar!/:5.6.15.Final]
	at org.hibernate.jpa.boot.internal.EntityManagerFactoryBuilderImpl.build(EntityManagerFactoryBuilderImpl.java:1494) [hibernate-core-5.6.15.Final.jar!/:5.6.15.Final]
	at org.springframework.orm.jpa.vendor.SpringHibernateJpaPersistenceProvider.createContainerEntityManagerFactory(SpringHibernateJpaPersistenceProvider.java:58) [spring-orm-5.3.31.jar!/:5.3.31]
	at org.springframework.orm.jpa.LocalContainerEntityManagerFactoryBean.createNativeEntityManagerFactory(LocalContainerEntityManagerFactoryBean.java:365) [spring-orm-5.3.31.jar!/:5.3.31]
	at org.springframework.orm.jpa.AbstractEntityManagerFactoryBean.buildNativeEntityManagerFactory(AbstractEntityManagerFactoryBean.java:409) [spring-orm-5.3.31.jar!/:5.3.31]
	at org.springframework.orm.jpa.AbstractEntityManagerFactoryBean.afterPropertiesSet(AbstractEntityManagerFactoryBean.java:396) [spring-orm-5.3.31.jar!/:5.3.31]
	at org.springframework.orm.jpa.LocalContainerEntityManagerFactoryBean.afterPropertiesSet(LocalContainerEntityManagerFactoryBean.java:341) [spring-orm-5.3.31.jar!/:5.3.31]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.invokeInitMethods(AbstractAutowireCapableBeanFactory.java:1863) [spring-beans-5.3.31.jar!/:5.3.31]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.initializeBean(AbstractAutowireCapableBeanFactory.java:1800) [spring-beans-5.3.31.jar!/:5.3.31]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.doCreateBean(AbstractAutowireCapableBeanFactory.java:620) [spring-beans-5.3.31.jar!/:5.3.31]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.createBean(AbstractAutowireCapableBeanFactory.java:542) [spring-beans-5.3.31.jar!/:5.3.31]
	at org.springframework.beans.factory.support.AbstractBeanFactory.lambda$doGetBean$0(AbstractBeanFactory.java:335) [spring-beans-5.3.31.jar!/:5.3.31]
	at org.springframework.beans.factory.support.DefaultSingletonBeanRegistry.getSingleton(DefaultSingletonBeanRegistry.java:234) ~[spring-beans-5.3.31.jar!/:5.3.31]
	at org.springframework.beans.factory.support.AbstractBeanFactory.doGetBean(AbstractBeanFactory.java:333) [spring-beans-5.3.31.jar!/:5.3.31]
	at org.springframework.beans.factory.support.AbstractBeanFactory.getBean(AbstractBeanFactory.java:208) [spring-beans-5.3.31.jar!/:5.3.31]
	at org.springframework.context.support.AbstractApplicationContext.getBean(AbstractApplicationContext.java:1168) ~[spring-context-5.3.31.jar!/:5.3.31]
	at org.springframework.context.support.AbstractApplicationContext.finishBeanFactoryInitialization(AbstractApplicationContext.java:919) ~[spring-context-5.3.31.jar!/:5.3.31]
	at org.springframework.context.support.AbstractApplicationContext.refresh(AbstractApplicationContext.java:591) ~[spring-context-5.3.31.jar!/:5.3.31]
	at org.springframework.boot.web.servlet.context.ServletWebServerApplicationContext.refresh(ServletWebServerApplicationContext.java:147) ~[spring-boot-2.7.18.jar!/:2.7.18]
	at org.springframework.boot.SpringApplication.refresh(SpringApplication.java:732) ~[spring-boot-2.7.18.jar!/:2.7.18]
	at org.springframework.boot.SpringApplication.refreshContext(SpringApplication.java:409) ~[spring-boot-2.7.18.jar!/:2.7.18]
	at org.springframework.boot.SpringApplication.run(SpringApplication.java:308) ~[spring-boot-2.7.18.jar!/:2.7.18]
	at org.springframework.boot.SpringApplication.run(SpringApplication.java:1300) ~[spring-boot-2.7.18.jar!/:2.7.18]
	at org.springframework.boot.SpringApplication.run(SpringApplication.java:1289) ~[spring-boot-2.7.18.jar!/:2.7.18]
	at com.example.library.LibraryApplication.main(LibraryApplication.java:9) ~[classes!/:0.0.1-SNAPSHOT]
	at sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method) ~[na:1.8.0_291]
	at sun.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62) ~[na:1.8.0_291]
	at sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43) ~[na:1.8.0_291]
	at java.lang.reflect.Method.invoke(Method.java:498) ~[na:1.8.0_291]
	at org.springframework.boot.loader.MainMethodRunner.run(MainMethodRunner.java:49) ~[library-management-0.0.1-SNAPSHOT.jar:0.0.1-SNAPSHOT]
	at org.springframework.boot.loader.Launcher.launch(Launcher.java:108) ~[library-management-0.0.1-SNAPSHOT.jar:0.0.1-SNAPSHOT]
	at org.springframework.boot.loader.Launcher.launch(Launcher.java:58) ~[library-management-0.0.1-SNAPSHOT.jar:0.0.1-SNAPSHOT]
	at org.springframework.boot.loader.JarLauncher.main(JarLauncher.java:65) ~[library-management-0.0.1-SNAPSHOT.jar:0.0.1-SNAPSHOT]

2026-05-28 01:07:25.823  INFO 23680 --- [           main] org.hibernate.dialect.Dialect            : HHH000400: Using dialect: org.hibernate.dialect.MySQLDialect
2026-05-28 01:07:26.351  INFO 23680 --- [           main] o.h.e.t.j.p.i.JtaPlatformInitiator       : HHH000490: Using JtaPlatform implementation: [org.hibernate.engine.transaction.jta.platform.internal.NoJtaPlatform]
2026-05-28 01:07:26.359  INFO 23680 --- [           main] j.LocalContainerEntityManagerFactoryBean : Initialized JPA EntityManagerFactory for persistence unit 'default'
2026-05-28 01:07:26.693  WARN 23680 --- [           main] JpaBaseConfiguration$JpaWebConfiguration : spring.jpa.open-in-view is enabled by default. Therefore, database queries may be performed during view rendering. Explicitly configure spring.jpa.open-in-view to disable this warning
2026-05-28 01:07:26.909  INFO 23680 --- [           main] o.s.b.w.embedded.tomcat.TomcatWebServer  : Tomcat started on port(s): 8080 (http) with context path ''
2026-05-28 01:07:26.915  INFO 23680 --- [           main] com.example.library.LibraryApplication   : Started LibraryApplication in 4.016 seconds (JVM running for 4.266)


stderr:

(empty)

## Notes

- Fallback test gate was used because Testing Agent did not return valid JSON.
- For Maven projects, compile/test/package/jar startup are verified.
