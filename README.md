# logAnalytics

# logAnalytics 개념
logAnalytics는 사용자가 미리 설정한 위치의 로그파일(log conf파일)을 읽고, 사용자가 사전에 정의한 분석 규칙(main conf파일)으로 로그를 분석하는 프로그램이다.
logAnalytics는 아래 두 가지 명령어를 제공한다.
<pre>
1) python3 util/utilmain.py
2) python3 src/main.py
</pre>

- utilmain.py: 분석할 로그의 다운로드, 압축해제, 및 분석할 로그의 경로를 설정한 파일(log conf파일) 생성기능 제공
- main.py: log conf파일에서 지정한 경로의 로그들을, main conf에서 지정한 규칙에 의해서 분석하는 기능 제공


# utilmain.py
사용 방법은 아래 명령어를 통해서 확인할 수 있다.
python3 util/utilmain.py -h

-u: 로그 다운로드 url, 예) http://www.log.com/mylog.tar.gz
-t: conf file template 경로, 예) res/logconftemplate.json
-c: 압축된 로그파일 경로(tar.gz 또는 tgz 파일만 지원), 예) /tmp/log.tar.gz
-d: 압축이 해제된 로그 디렉토리 경로, 예) /tmp/log

-u 옵션은 -d, -t 옵션과 함께 사용한다.
```
예) python3 utilmain.py -u <download url> -s <download directory path> -t <conf file template>
```

-c 옵션는 -d, -t 옵션과 함께 사용한다.
```
예) python3 utilmain.py -c <compressed file path> -d <destination directory path> -t <conf file template>
```

-d 옵션은 -t 옵션과 함께 사용한다.
```
예) python3 utilmain.py -d <destination directory path> -t <conf file template>
```

conf file template은 압축이 히제된 로그 디렉토리에서, 확인해야할 로그 파일 리스트가 저장된 파일이다.
신규로 분석이 필요한 파일이 있는 경우, conf file template에 분석할 로그파일의 경로를 추가 및 수정할 수 있다.


# main.py
사용 방법은 아래 명령어를 통해서 확인할 수 있다.
```
python3 util/utilmain.py -h
```

```
-l: log conf 파일의 위치를 넣는다. log conf 파일은 utilmain.py를 실행시키면 생성된다. 예) logs/logconf.json
-c: main conf 파일의 위치를 넣는다. main conf 파일은 사용자가 작성한 파일이다. 예) res/mainconf.json
```

log conf파일경로가 logs/logconf.json이고, main conf 파일의 경로가 res/mainconf.json 이면 아래와 같이 프로그램을 실행할 수 있다.
```
python3 src/main.py -l logs/logconf.json -c res/mainconf.json
```

# 사용 예제
## 로그 파일을 다운로드 받아야 하는 경우

1. 다운로드 디렉토리 생성
```
$ mkdir ./logs
```

3. 로그파일 다운로드 및 압축해제
```
$ python3 util/utilmain.py -u http://db.log.com/logs/mylog.tgz -s logs -t res/logconftemplate.json
```

4. 위에서 생성된 logconf.json (분석할 로그 경로)파일과 mainconf.json(분석 규칙)파일을 사용하여 로그 분석
```
$ python3 src/main.py -l logs/logconf.json -c res/mainconf.json
```


## 로그파일이 압축된 상태로 존재하는 경우

1. 압축된 로그파일(mylog.tgz)을 압축 해제(logs/)
```
$ python3 util/utilmain.py -c logs/mylog.tgz -d logs -t res/logconftemplate.json
....
logs/logconf.json  is generated
```

2. 위에서 생성된 logconf.json (분석할 로그 경로)파일과 mainconf.json(분석 규칙)파일을 사용하여 로그 분석
```
$ python3 src/main.py -l logs/logconf.json -c res/mainconf.json
```


## 압축해제 된 로그파일이 있는 경우
1. logconf.json 파일만 생성
```
$ python3 util/utilmain.py -d logs -t res/logconftemplate.json
...
logs/logconf.json  is generated
```


2. 위에서 생성된 logconf.json (분석할 로그 경로)파일과 mainconf.json(분석 규칙)파일을 사용하여 로그 분석
```
$ python3 src/main.py -l logs/logconf.json -c res/mainconf.json
```


## 분석 결과 예제
```
==== matched log by composite Rule ====
......
Result
문제 아님, 정상 동작
```


## 출력 데이터 확인 방법
==== matched log by Oneshut Rule ====
- mainconf.json의 OneshutRule로 정의한 규칙에 의해서 필터링된 로그 정보가 출력됨

==== matched log by composite Rule ====
- mainconf.json의 CompositeRule로 정의한 규칙에 의해서 필터링된 로그 정보가 출력됨

==== Faulty Logs ====
- mainconf.json의 OneshutRule 에서 필터링된 로그 중 logType을 FAULT로 정의한 로그가 출력됨 

==== Composite faulty Logs  ====
- mainconf.json의 CompositeRule에 의해서 필터링된 로그 중 logType을 FAULT로 정의한 로그가 출력됨 

==== Detected abnomal states ====
- mainconf.json으로 확인되지 않은 규칙들 중, logType이 NORMAL인 필터링 규칙들을 출력함
- 로그가 남아있을 것으로 예상하고 있지만, 실제로는 찾지 못한 로그들에 대해서 보여줌


# conf file template(res/logconftemplate.json) 작성 방법
res/logconftemplate.json 파일을 열어보면 다음과 같이
분석해야하는 로그파일 경로가 들어있다.

<pre>
<code>
{
    "path" : [
        "log/file/path.txt"
    ]
}
</pre>
</code>


"path"의 value로 되어있는 json array는 분석해야할 로그파일의 경로를 나타낸다.
이 경로는 추후에, 실제 log conf 파일을 생성할 때 사용된다.
위와 같이 "log/file/path.txt" 하나의 path가 기록된 res/logconftemplate.json 파일로는 
아래와 같은 logconf.json 파일이 생성된다.

<pre>
<code>
{
    "targets": [
        "downloadedDir/log/file/path.txt"
    ]
}
</pre>
</code>

로그를 다운로드 받은 위치가 downloadedDir 이고 res/logconftemplate.json 파일에 path가 log/file/path.txt로 되어있으면
downloadedDir/log/file/path.txt 로 경로가 결정된다.
실제 로그를 분석할 때, python3 src/main.py 프로그램에서 logconf.json에 기록된 파일 리스트를 읽고 로그를 분석하게 된다.

따라서 사용자가 res/logconftemplate.json 파일에 기록된 로그 경로를 수정고, python3 util/utilmain.py 프로그램을 실행시키면
수정된 logconf.json 파일을 생성할 수 있다.



# 로그 분석 규칙 (mainconf.json) 작성 방법
res/mainconf.json 아래와 같은 로그 분석 규칙 정보가 작성되어 있다.
<pre>
<code>
{
	"OneShutRule": [{
			"id": "id_string_1",
			"filter": ["regular expression for filtering"],
			"result": "Your program is normally run",
			"outputType": "TEXT",
			"logType": "NORMAL"
		},
		{
			"id": "id_string_2",
			"filter": ["regular", "expression", "for", "filtering"],
			"result": "path/for/file/descriptino.txt",
			"outputType": "FILE",
			"logType": "FAULT"
		},
		{
			"id": "id_string_3",
			"filter": ["input", "your", "data", "to", "check", "a line"],
			"result": "You can find a fault in the log line",
			"outputType": "TEXT",
			"logType": "FAULT"
		}
	],
	"CompositeRule": [
		{
			"id": "boolean_expression_rule",
			"condition": "id_string_1 and id_string_2 and not id_string_3",
			"result": "testdata/result.txt",
			"ruleType": "BOOLEANEXPR",
			"outputType": "FILE",
			"logType": "FAULT"
		},
		{
			"id": "sequential_rule",
			"order": ["id_string_1", "id_string_2"],
			"result": "This is NOT a bug",
			"ruleType": "SEQUENTIAL",
			"outputType": "TEXT",
			"logType": "NORMAL"
		}
	]
}
</pre>
</code>


1) OneShutRule
  - OneShutRule의 배열에 포함되는 각 json 객체들은 각각의 로그 라인에 대한 분석 규칙을 정의함
  - id: 검색 규칙 아이디(식별정보)
  - filter: 검색 필터로 지정할 문자열, 정규식 사용 가능
  - result: filter에 의해서 로그가 검색된 경우, 해당 로그에 대한 설명
  - outputType: result값 종류,
     - TEXT: result가 text 형식으로 작성되어 있는 경우 사용
     - FILE: result에 text대신 파일 경로를 넣은 경우 사용, 로그 분석결과를 출력할 때 지정한 위치의 파일에 작성된 데이터를 출력함
  - logType: 로그의 의미 (결함, 정상)을 판별하는 식별정보
     - NORMAL: 정상인 경우에 출력하는 로그
     - FAULT: 결함이 발생한 경우 출력하는 로그
 
2) CompositeRule
  - OneShutRule에서 정의한 개별 규칙들의 의존관계에 의해서 정의되는 로그 분석 규칙:
  - id:  CompositeRule 에 대한 아이디
  - condition: ruleType이 "BOOLEANEXPR"인 경우에 사용되는 값으로, OneShutRule의 아이디를 기준으로 boolean expression을 문자열로 기술한다.
  - order: ruleType이 "SEQUENTIAL"인 경우에 적용되는 값으로, 매칭되는 로그의 순서를 기술한다. 배열 순서로 기술함
          예) ["id_string_1", "id_string_2"]는 "id_string_1" rule이 먼저 매칭되고, "id_string_2" rule이 다음에 매칭되는 조건을 정의함
  - ruleType: "BOOLEANEXPR"과 "SEQUENTIAL"의 두 가지 값을 가질 수 있음, "BOOLEANEXPR"은 OneShutRule간에 논리관계에 의한 의존성이 있는경우, "SEQUENTIAL"은 OneShutRule간에 순서 의존성이 있는 경우, 
  - result: 조건과 매칭되는 로그가 검색된 경우, 해당 로그에 대한 설명
  - 그외: outputType, logType은 OneShutRule과 동일함
