import typing
from pydantic import BaseModel, Field


class BookInfo(BaseModel):
    novelId: typing.Optional[str] = None
    novelName: typing.Optional[str] = None
    authorId: typing.Optional[str] = None
    authorName: typing.Optional[str] = None
    novelClass: typing.Optional[str] = None
    novelTags: typing.Optional[str] = None
    novelTagsId: typing.Optional[str] = None
    novelCover: typing.Optional[str] = None
    originalCover: typing.Optional[str] = None
    novelStep: typing.Optional[str] = None
    novelIntro: typing.Optional[str] = None
    novelIntroShort: typing.Optional[str] = None
    isVip: typing.Optional[str] = None
    isPackage: typing.Optional[str] = None
    novelSize: typing.Optional[str] = None
    novelsizeformat: typing.Optional[str] = None
    novelChapterCount: typing.Optional[str] = None
    renewDate: typing.Optional[str] = None
    renewChapterId: typing.Optional[str] = None
    renewChapterName: typing.Optional[str] = None
    novelScore: typing.Optional[str] = None
    islock: typing.Optional[str] = None
    novelbefavoritedcount: typing.Optional[str] = None
    novelbefavoritedcountformat: typing.Optional[str] = None
    type_id: typing.Optional[str] = None
    age: typing.Optional[str] = None
    maxChapterId: typing.Optional[str] = None
    chapterdateNewest: typing.Optional[str] = None
    local: typing.Optional[str] = None
    localImg: typing.Optional[str] = None
    novelStyle: typing.Optional[str] = None
    series: typing.Optional[str] = None
    protagonist: typing.Optional[str] = None
    costar: typing.Optional[str] = None
    other: typing.Optional[str] = None
    comment_count: typing.Optional[str] = None
    nutrition_novel: typing.Optional[str] = None
    ranking: typing.Optional[str] = None
    novip_clicks: typing.Optional[str] = None
    vipChapterid: typing.Optional[str] = None
    isSign: typing.Optional[str] = None
    ILTC: typing.Optional[str] = None
    mainview: typing.Optional[str] = None
    codeUrl: typing.Optional[str] = None
    novelReviewScore: typing.Optional[str] = None
    authorsayrule: typing.Optional[str] = None
    copystatus: typing.Optional[str] = None


class ChapterInfo(BaseModel):
    novelid: typing.Optional[str] = None
    chapterid: typing.Optional[str] = None
    chaptertype: typing.Optional[str] = None
    chaptername: typing.Optional[str] = None
    chapterdate: typing.Optional[str] = None
    chapterclick: typing.Optional[str] = None
    chaptersize: typing.Optional[str] = None
    chapterintro: typing.Optional[str] = None
    islock: typing.Optional[str] = None
    islockMessage: typing.Optional[str] = None
    isvip: typing.Optional[int] = None
    point: typing.Optional[int] = None
    originalPrice: typing.Optional[int] = None
    pointfreevip: typing.Optional[int] = None
    isProtect: typing.Optional[int] = None
    originalPriceMessage: typing.Optional[str] = None
    pointMeassge: typing.Optional[str] = None
    chapterMessage: typing.Optional[str] = None
    lastpost_time: typing.Optional[str] = None
    examineMessage: typing.Optional[str] = None
    isEdit: typing.Optional[str] = None
    message: typing.Optional[str] = None
    thank: typing.Optional[int] = None
    ticketStarttime: typing.Optional[str] = None
    ticketEndtime: typing.Optional[str] = None
    draft: typing.Optional[dict] = None
    manageExplain: typing.Optional[list] = None
    cache_file_path: typing.Optional[str] = None


class ContentInfo(BaseModel):
    chapterId: typing.Optional[str] = None
    chapterName: typing.Optional[str] = None
    chapterIntro: typing.Optional[str] = None
    chapterSize: typing.Optional[str] = None
    chapterDate: typing.Optional[str] = None
    sayBody: typing.Optional[str] = None
    upDown: typing.Optional[str] = None
    update: typing.Optional[str] = None
    content: typing.Optional[str] = None
    isvip: typing.Optional[str] = None
    authorid: typing.Optional[str] = None
    autobuystatus: typing.Optional[str] = None
    noteislock: typing.Optional[str] = None


class SearchInfo(BaseModel):
    novel_id: typing.Optional[str] = Field(None, alias="novelid")
    novel_name: typing.Optional[str] = Field(None, alias="novelname")
    author_name: typing.Optional[str] = Field(None, alias="authorname")
    novelintroshort: typing.Optional[str] = None
    novelstep: typing.Optional[str] = None
    type_id: typing.Optional[str] = None
    authorid: typing.Optional[str] = None
    reviewrank: typing.Optional[str] = None
    reviewnum: typing.Optional[str] = None
    tags: typing.Optional[str] = None
    ebookurl: typing.Optional[str] = None
    novelborndate: typing.Optional[str] = None
    novelsize: typing.Optional[str] = None
    reviewscore: typing.Optional[str] = None
    age: typing.Optional[str] = None
    novelreviewexplain: typing.Optional[str] = None
    filmname: typing.Optional[str] = None
    filmtype: typing.Optional[str] = None
    filmtext: typing.Optional[str] = None
    filmlabel: typing.Optional[str] = None
    cover: typing.Optional[str] = None
    local: typing.Optional[str] = None
    localImg: typing.Optional[str] = None
    novelClass: typing.Optional[str] = None
    novelSizeformat: typing.Optional[str] = None
    novelintro: typing.Optional[str] = None
    favoriteStatus: typing.Optional[str] = None
