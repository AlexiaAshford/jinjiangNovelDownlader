from pydantic import typing
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BookInfoSql(Base):
    __tablename__ = 'bookinfo'
    novelId: typing.Optional[str] = Column(Integer, primary_key=True)
    novelName: typing.Optional[str] = Column(String)
    authorId: typing.Optional[str] = Column(String)
    authorName: typing.Optional[str] = Column(String)
    novelClass: typing.Optional[str] = Column(String)
    novelTags: typing.Optional[str] = Column(String)
    novelTagsId: typing.Optional[str] = Column(String)
    novelCover: typing.Optional[str] = Column(String)
    originalCover: typing.Optional[str] = Column(String)
    novelStep: typing.Optional[str] = Column(String)
    novelIntro: typing.Optional[str] = Column(String)
    novelIntroShort: typing.Optional[str] = Column(String)
    isVip: typing.Optional[str] = Column(String)
    isPackage: typing.Optional[str] = Column(String)
    novelSize: typing.Optional[str] = Column(String)
    novelsizeformat: typing.Optional[str] = Column(String)
    novelChapterCount: typing.Optional[str] = Column(String)
    renewDate: typing.Optional[str] = Column(String)
    renewChapterId: typing.Optional[str] = Column(String)
    renewChapterName: typing.Optional[str] = Column(String)
    novelScore: typing.Optional[str] = Column(String)
    islock: typing.Optional[str] = Column(String)
    novelbefavoritedcount: typing.Optional[str] = Column(String)
    novelbefavoritedcountformat: typing.Optional[str] = Column(String)
    type_id: typing.Optional[str] = Column(String)
    age: typing.Optional[str] = Column(String)
    maxChapterId: typing.Optional[str] = Column(String)
    chapterdateNewest: typing.Optional[str] = Column(String)
    local: typing.Optional[str] = Column(String)
    localImg: typing.Optional[str] = Column(String)
    novelStyle: typing.Optional[str] = Column(String)
    series: typing.Optional[str] = Column(String)
    protagonist: typing.Optional[str] = Column(String)
    costar: typing.Optional[str] = Column(String)
    other: typing.Optional[str] = Column(String)
    comment_count: typing.Optional[str] = Column(String)
    nutrition_novel: typing.Optional[str] = Column(String)
    ranking: typing.Optional[str] = Column(String)
    novip_clicks: typing.Optional[str] = Column(String)
    vipChapterid: typing.Optional[str] = Column(String)
    isSign: typing.Optional[str] = Column(String)
    ILTC: typing.Optional[str] = Column(String)
    mainview: typing.Optional[str] = Column(String)
    codeUrl: typing.Optional[str] = Column(String)
    novelReviewScore: typing.Optional[str] = Column(String)
    authorsayrule: typing.Optional[str] = Column(String)
    copystatus: typing.Optional[str] = Column(String)

    def dict(self):
        # delete sqlalchemy object attribute. Otherwise, it will cause an error when converting to json
        if "_sa_instance_state" in self.__dict__:
            self.__dict__.pop("_sa_instance_state")
        return self.__dict__


class ChapterSql(Base):
    __tablename__ = 'chapterinfo'
    id: typing.Optional[str] = Column(Integer, primary_key=True, autoincrement=True)
    is_vip: typing.Optional[str] = Column(String)
    novelId: typing.Optional[str] = Column(Integer, nullable=True)
    chapterid: typing.Optional[str] = Column(String)
    chapter_name: typing.Optional[str] = Column(String, nullable=True)
    chapter_content: typing.Optional[str] = Column(String, nullable=True)


class CatalogueSql(Base):
    __tablename__ = 'catalogue'
    id: typing.Optional[str] = Column(Integer, primary_key=True, autoincrement=True)
    novelid: typing.Optional[str] = Column(Integer)
    chapterid: typing.Optional[str] = Column(String)
    chaptername: typing.Optional[str] = Column(String)
    chaptersize: typing.Optional[str] = Column(String)
    chapterintro: typing.Optional[str] = Column(String)
    islock: typing.Optional[str] = Column(String)
    islockMessage: typing.Optional[str] = Column(String)
    isvip: typing.Optional[str] = Column(String)
    point: typing.Optional[str] = Column(String)
    originalPrice: typing.Optional[str] = Column(String)
    pointfreevip: typing.Optional[str] = Column(String)
    lastpost_time: typing.Optional[str] = Column(String)
