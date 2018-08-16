USE jobbole;

DROP TABLE IF EXISTS `article`;

CREATE TABLE `article` (
    `title` varchar(200) NOT NULL, -- 文章标题
    `create_time` date, -- 创建日期
    `url` varchar(300) NOT NULL, -- 文章 url
    `url_object_id` varchar(50) NOT NULL, -- url 对应的随机字符串
    `front_image_url` varchar(300), -- 封面图片 url
    `front_image_path` varchar(200), -- 封面图片保存路径
    `praise_num` int(11) DEFAULT 0, -- 赞数
    `comm_num` int(11) DEFAULT 0, -- 评论数
    `fav_num` int(11) DEFAULT 0, -- 收藏数
    `tags` varchar(200), -- 标签
    `content` longtext, -- 文章内容
    PRIMARY KEY (`url_object_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;