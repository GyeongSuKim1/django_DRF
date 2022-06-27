from django.db import models


class product(models.Model):
    user = models.ForeignKey('user.User', verbose_name="작성자", on_delete=models.CASCADE)
    title = models.CharField("제목", max_length=50)
    thumbnail = models.FileField("썸네일", upload_to="product/")  # 테스트를 위해 임시로 경로 지정
    description = models.TextField("설명", max_length=300)

    created = models.DateTimeField("등록일자", auto_now_add=True)
    exposure_start_date = models.DateField("노출 시작 일자",)
    exposure_end_date = models.DateField("노출 종료 일자",)