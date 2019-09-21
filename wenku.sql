/*
Navicat MySQL Data Transfer

Source Server         : wenku
Source Server Version : 50644
Source Host           : 45.248.86.152:3306
Source Database       : wenku

Target Server Type    : MYSQL
Target Server Version : 50644
File Encoding         : 65001

Date: 2019-09-21 15:57:30
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for chongzhi
-- ----------------------------
DROP TABLE IF EXISTS `chongzhi`;
CREATE TABLE `chongzhi` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `qq` varchar(255) DEFAULT NULL,
  `count` int(11) DEFAULT NULL,
  `time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `qq` (`qq`),
  CONSTRAINT `qq` FOREIGN KEY (`qq`) REFERENCES `wk_user` (`qq`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for direct_return
-- ----------------------------
DROP TABLE IF EXISTS `direct_return`;
CREATE TABLE `direct_return` (
  `id` int(255) NOT NULL AUTO_INCREMENT,
  `url` varchar(255) DEFAULT NULL,
  `download_path` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for new_friend
-- ----------------------------
DROP TABLE IF EXISTS `new_friend`;
CREATE TABLE `new_friend` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `qq` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for wk_download
-- ----------------------------
DROP TABLE IF EXISTS `wk_download`;
CREATE TABLE `wk_download` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `qq` varchar(255) DEFAULT NULL,
  `url` varchar(255) DEFAULT NULL,
  `download_path` varchar(255) DEFAULT NULL,
  `download_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `dd` (`qq`),
  CONSTRAINT `dd` FOREIGN KEY (`qq`) REFERENCES `wk_user` (`qq`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for wk_user
-- ----------------------------
DROP TABLE IF EXISTS `wk_user`;
CREATE TABLE `wk_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `qq` varchar(255) DEFAULT NULL,
  `download_count` int(11) DEFAULT NULL,
  `remain` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `qq` (`qq`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8;
