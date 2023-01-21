FROM openjdk:11 as builder

WORKDIR /work

COPY ProcessUnits.java /work/

RUN mkdir -p units
RUN wget https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-core/1.2.1/hadoop-core-1.2.1.jar
RUN javac -classpath hadoop-core-1.2.1.jar -target 8 -source 8 -d units ProcessUnits.java
RUN jar -cvf units.jar -C units/ .

FROM apache/hadoop:3

# little hack for hadoop
USER root

WORKDIR /app

COPY sample.txt /app/
COPY run.sh /app/
COPY --from=builder /work/ /app/

ENTRYPOINT [ "bash", "run.sh" ]