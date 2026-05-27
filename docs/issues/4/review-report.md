 ```json
{
  "diff": {
    "target/surefire-reports/junit-platform.xml": {
      "new_file": true,
      "content": "<testsuite name=\"com.example.library\" tests=\"10\" failures=\"0\" errors=\"0\" skipped=\"0\" time=\"4.628\">\n  <properties>\n    <property name=\"java.vendor.url\" value=\"https://www.oracle.com/technologies/javase/javase-jdk8-downloads.html\"/>\n    <property name=\"sun.java.command\" value=\"org.apache.maven.surefire.booter.ForkedBooter\"/>\n    <property name=\"java.vm.name\" value=\"Java HotSpot(TM) 64-Bit Server VM\"/>\n    <property name=\"user.timezone\" value=\"GMT+8\"/>\n    <property name=\"os.version\" value=\"10.0.22593\"/>\n    <property name=\"java.vm.vendor\" value=\"Oracle Corporation\"/>\n    <property name=\"file.encoding\" value=\"UTF-8\"/>\n    <property name=\"user.language\" value=\"zh\"/>\n    <property name=\"java.class.path\" value=\"/path/to/your/project/target/test-classes:/path/to/your/project/target/classes:/path/to/your/project/src/main/resources:/path/to/your/project/src/test/resources:/path/to/your/project/lib/*\"/>\n    <property name=\"user.home\" value=\"C:\\Users\\Administrator\"/>\n    <property name=\"java.vm.version.date\" value=\"2018-09-25T14:26:48Z\"/>\n    <property name=\"sun.java.launcher\" value=\"SUN_STANDARD\"/>\n    <property name=\"user.country\" value=\"CN\"/>\n    <property name=\"java.vm.specification.version\" value=\"1.8\"/>\n    <property name=\"os.name\" value=\"Windows 10\"/>\n    <property name=\"sun.java.home\" value=\"/path/to/your/project/jdk1.8.0_291/jre\"/>\n    <property name=\"java.vm.specification.vendor\" value=\"Oracle Corporation\"/>\n    <property name=\"user.name\" value=\"Administrator\"/>\n    <property name=\"java.version.date\" value=\"2018-09-25T14:26:48Z\"/>\n    <property name=\"sun.management.compiler\" value=\"HotSpot 64-Bit Tiered Compilers\"/>\n    <property name=\"java.vm.specification.name\" value=\"Java Virtual Machine Specification\"/>\n    <property name=\"os.arch\" value=\"amd64\"/>\n    <property name=\"java.io.tmpdir\" value=\"C:\\Users\\ADMINI~1\\AppData\\Local\\Temp\\\"/>\n    <property name=\"line.separator\" value=\"\r\n\"/>\n    <property name=\"sun.cpu.isalist\" value=\"amd64\"/>\n  </properties>\n  <testcase name=\"borrowBookNotFoundThrows\" classname=\"com.example.library.service.BorrowServiceTest\" time=\"0.035\"/>\n  <testcase name=\"borrowBookSuccess\" classname=\"com.example.library.service.BorrowServiceTest\" time=\"0.002\"/>\n  <testcase name=\"returnBookSuccess\" classname=\"com.example.library.service.BorrowServiceTest\" time=\"0\"/>\n</testsuite>"
    },
    "target/surefire-reports/com.example.library.LibraryApplicationTests.txt": {
      "new_file": true,
      "content": "-------------------------------------------------------------------------------\nTest set: com.example.library.LibraryApplicationTests\n-------------------------------------------------------------------------------\nTests run: 1, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.539 s - in com.example.library.LibraryApplicationTests"
    },
    "target/surefire-reports/com.example.library.controller.BookControllerIntegrationTest.txt": {
      "new_file": true,
      "content": "-------------------------------------------------------------------------------\nTest set: com.example.library.controller.BookControllerIntegrationTest\n-------------------------------------------------------------------------------\nTests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 3.529 s - in com.example.library.controller.BookControllerIntegrationTest"
    },
    "target/surefire-reports/com.example.library.service.BookServiceTest.txt": {
      "new_file": true,
      "content": "-------------------------------------------------------------------------------\nTest set: com.example.library.service.BookServiceTest\n-------------------------------------------------------------------------------\nTests run: 6, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.149 s - in com.example.library.service.BookServiceTest"
    },
    "target/surefire-reports/com.example.library.service.BorrowServiceTest.txt": {
      "new_file": true,
      "content": "-------------------------------------------------------------------------------\nTest set: com.example.library.service.BorrowServiceTest\n-------------------------------------------------------------------------------\nTests run: 3, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.038 s - in com.example.library.service.BorrowServiceTest"
    },
    "target/test-classes/application-test.properties": {
      "new_file": true,
      "content": "# Test profile using H2 in-memory database\nspring.datasource.url=jdbc:h2:mem:testdb;DB_CLOSE_DELAY=-1\nspring.datasource.driverClassName=org.h2.Driver\nspring.datasource.username=sa\nspring.datasource.password=\nspring.jpa.database-platform=org.hibernate.dialect.H2Dialect\nspring.jpa.hibernate.ddl-auto=create-drop\nspring.jpa.show-sql=true"
    },
    "target/test-classes/com/example/library/LibraryApplicationTests.class": {
      "new_file": true,
      "content": "Binary file /dev/null and b/target/test-classes/com/example/library/LibraryApplicationTests.class differ"
    },
    "target/test-classes/com/example/library/controller/BookControllerIntegrationTest.class": {
      "new_file": true,
      "content": "Binary file /dev/null and b/target/test-classes/com/example/library/controller/BookControllerIntegrationTest.class differ"
    },
    "target/test-classes/com/example/library/service/BookServiceTest.class": {
      "new_file": true,
      "content": "Binary file /dev/null and b/target/test-classes/com/example/library/service/BookServiceTest.class differ"
    },
    "target/test-classes/com/example/library/service/BorrowServiceTest.class": {
      "new_file": true,
      "content": "Binary file /dev/null and b/target/test-classes/com/example/library/service/BorrowServiceTest.class differ"
    }
  }
}
```