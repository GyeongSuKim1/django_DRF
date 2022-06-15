# 개념정리

  > # *args
  > > - *args는 가변 인자를 위한 변수
  > > - 듀플 형태로 값을 받아옴
  ```python
  def num(name,*args):
    total = 0
    for i in args:
        total += i
    print(f'{name}의 시험 평균은 :{total / 4} 입니다')
    return

score = (72, 88, 96, 92)

num("고길동", *score)

# ㅡㅡ 출력 값 ㅡㅡ
# 고길동의 시험 평균은 :87.0입니다
  ```
  
  > # **kwargs
  > > - 딕셔너리 형태로 값을 받아옴
```python
def num(**kwargs):
    for key, value in kwargs.items():
        print(f'키 값 :{key}, 벨류 값 :{value}')
    return

num (
    key ="value",
    one=1,
    two=2,
    three=3,
)

# ㅡㅡ 출력 값 ㅡㅡ
# 키값 :key, 벨류 값 :value,
# 키값 :one, 벨류 값 :1,
# 키값 :tow, 벨류 값 :2,
# 키값 :three, 벨류 값 :3,
```

  > # *args,**kwargs를 사용한 예제 코드
  ```python
  def user_info(*args, **kwargs):
    for arg in args:
        print(arg)
    for key, value in kwargs.items():
        print(f'{key}:{value}')

args = ('user1', 'user2', 'user3', 'user4')
    
kwargs={
    "name":"Gildong Lee",
    "number":"010-1111-1111",
    "address":"amazon",
    "info":"Soo Good~",
}
user_info(*args, **kwargs)

# user1
# user2
# user3
# user4
# name:Gildong Lee
# number:010-1111-1111
# address:amazon
# info:Soo Good~
```

  > # mutable과 immutable
  > > - mutable
  > >   - 변경되는 객체 (객체의 상태를 변경할 수 있음)
  > >   - 모든 객체를 각각 생성해서 참조해 줌
  > >   - list, set, dictionary 가 있음
  > >
  > > - immutable
  > >   - 변경되지 않는 객체(객체의 상태를 병경할 수 없음)
  > >   - 객체의 값이 같은 경우에 변수에 상관없이 동일한 곳을 참조
  > >   - int, float, tuple, str, bool 이 있음

  > # DB Field 내의 Key 종류
  > > - Primary key(기본키) :
  > >   - 기본키(Primary key)는 쉽게 말해 유일무이한 값을 가진 키라고 생각할 수 있다. 쉽게 말하면 나의 이름 '김경수'를 예로 들수 있는데 우리나라에 '김경수'는 나 혼자 만이 아닐 것 이다. 따라서 여러명의 '김경수'를 구분하기 위해 주민등록번호를 사용한다. 여기서 이 주민등록 번호가 기본키라고 이해하면 쉽게 생각할 수 있다.
  > > - Candidate key(후보키) :
  > >   - 후보키(Candidate key)는 키본키의 부분집합이라고 할 수 있다. 앞서 말한 여러명의 '김경수'를 주민등록번호로 구별한다. 그런데 이 '김경수'는 휴대폰번호를 이용해서 또한 구별이 가능하다. 결국 후보키는 말 그대로 기본키가 될 수 있는 후보키인 것이다. 
  > > - Alternate key(대체키) :
  > >   - 대체키(Alternate key)는 후보키가 둘 이상일 때 기본키를 제외한 나머지 후보키 들을 말함.
  > > - Foreign key(외래키) :
  > >   - 외래키(Foreign key)는 관계를 맺고 있는 릴레이션 R1, R2에서 릴레이션 R1이 참고하고 있는 릴레이션 R2의 기본키와 같은 R1 릴레이션의 속성을 외래키라고 한다. 즉 관련이 있는 여러 테이블들 사이에서 데이터의 일관성을 보장해 주는 수단이자, 두개의 테이블을 연결해 관계를 맺어주는 기준이 되는 키를 말한다.

> # Django에서 Queryset과 Object의 차이점
> > - Queryset 이란 ? 
> >   - Queryset은 데이터베이스에서 전달받은 객체들의 list
> >   - 각 객체들은 DB에서 하나의 record(row)에 해당 함
> >   - python으로 작성한 코드가 SQL로 mapping되어 Queryset이라는 자료 형태로 값이 넘어 옴
> >   - ORM 코드가 객체를 불러오지만 실제 DB에 쿼리가 이뤄지는 것은 아니다
> >   - Queryset의 lazy한 특성으로 인해 실제 데이터를 가져오기 위해서는 iterate시켜야 함
> > 
> > >  그렇다면 Queryset과 Object의 가장 큰 차이점은 데이터를 불러오는 방식이다. <br>
> > >  Django에서 Object의 데이터는 .get()으로 가져오고 <br>
> > >  Queryset은 .filter()로 데이터를 가져온다. <br>
> > >  <br>
> > >  또한 만약 get으로 해당 데이터를 불러올때 해당 데이터가 없다면 에러가 나지만, Queryset은 데이터가 존재하지 않더라도 빈 리스트        로 가져와서 정상적으로 작동이 된다. 때문에 .get은 try 예외처리를 함께 작성해주어야 데이터가 존재하지 않을때의 에러를 방지할        수 있다.
