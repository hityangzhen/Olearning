-- MySQL dump 10.13  Distrib 5.1.69, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: olearning
-- ------------------------------------------------------
-- Server version	5.1.69-0ubuntu0.11.10.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `admin_administrator`
--

DROP TABLE IF EXISTS `admin_administrator`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `admin_administrator` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `administrator_username` varchar(20) NOT NULL,
  `administrator_email` varchar(40) NOT NULL,
  `administrator_realname` varchar(20) NOT NULL,
  `administrator_tele` varchar(11) NOT NULL,
  `administrator_status` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin_administrator`
--

LOCK TABLES `admin_administrator` WRITE;
/*!40000 ALTER TABLE `admin_administrator` DISABLE KEYS */;
/*!40000 ALTER TABLE `admin_administrator` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `admin_coursetype`
--

DROP TABLE IF EXISTS `admin_coursetype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `admin_coursetype` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `coursetype_name` varchar(20) NOT NULL,
  `coursetype_positionid` varchar(20) NOT NULL,
  `coursetype_status` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin_coursetype`
--

LOCK TABLES `admin_coursetype` WRITE;
/*!40000 ALTER TABLE `admin_coursetype` DISABLE KEYS */;
INSERT INTO `admin_coursetype` VALUES (1,'java课程','java',0),(2,'大数据','DSJ',1),(3,'算法','SF',1),(4,'嵌入式','QRS',1);
/*!40000 ALTER TABLE `admin_coursetype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `admin_student`
--

DROP TABLE IF EXISTS `admin_student`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `admin_student` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `student_username` varchar(20) NOT NULL,
  `student_userpwd` varchar(20) NOT NULL,
  `student_email` varchar(40) NOT NULL,
  `student_tele` varchar(11) NOT NULL,
  `student_department` varchar(30) NOT NULL,
  `student_position` varchar(30) NOT NULL,
  `student_gender` tinyint(1) NOT NULL,
  `student_age` int(11) NOT NULL,
  `student_head_portrait` varchar(100) DEFAULT NULL,
  `student_identity` varchar(18) NOT NULL,
  `student_remark` varchar(500) DEFAULT NULL,
  `student_status` tinyint(1) NOT NULL,
  `student_positionid` varchar(20) NOT NULL,
  `student_ischecked` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin_student`
--

LOCK TABLES `admin_student` WRITE;
/*!40000 ALTER TABLE `admin_student` DISABLE KEYS */;
/*!40000 ALTER TABLE `admin_student` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `admin_task`
--

DROP TABLE IF EXISTS `admin_task`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `admin_task` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `task_name` varchar(50) NOT NULL,
  `coursetype_id` int(11) NOT NULL,
  `task_courseids` varchar(50) NOT NULL,
  `task_exercisepaperids` varchar(100) DEFAULT NULL,
  `task_starttime` datetime NOT NULL,
  `task_endtime` datetime NOT NULL,
  `task_status` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `admin_task_54fb2301` (`coursetype_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin_task`
--

LOCK TABLES `admin_task` WRITE;
/*!40000 ALTER TABLE `admin_task` DISABLE KEYS */;
/*!40000 ALTER TABLE `admin_task` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `admin_teacher`
--

DROP TABLE IF EXISTS `admin_teacher`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `admin_teacher` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `teacher_username` varchar(20) NOT NULL,
  `teacher_userpwd` varchar(20) NOT NULL,
  `teacher_email` varchar(40) NOT NULL,
  `teacher_tele` varchar(11) NOT NULL,
  `teacher_department` varchar(30) NOT NULL,
  `teacher_identity` varchar(18) NOT NULL,
  `teacher_realname` varchar(30) NOT NULL,
  `teacher_gender` tinyint(1) NOT NULL,
  `teacher_age` int(11) NOT NULL,
  `teacher_head_portrait` varchar(100) DEFAULT NULL,
  `teacher_remark` varchar(500) DEFAULT NULL,
  `teacher_status` tinyint(1) NOT NULL,
  `teacher_ischecked` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin_teacher`
--

LOCK TABLES `admin_teacher` WRITE;
/*!40000 ALTER TABLE `admin_teacher` DISABLE KEYS */;
INSERT INTO `admin_teacher` VALUES (1,'yiranyaoqiu','abcde123456','1491634755@qq.com','15228810828','培训部','320282199207273833','杨振',1,22,NULL,NULL,1,1);
/*!40000 ALTER TABLE `admin_teacher` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`),
  KEY `auth_group_permissions_bda51c3c` (`group_id`),
  KEY `auth_group_permissions_1e014c8f` (`permission_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  KEY `auth_permission_e4470c6e` (`content_type_id`)
) ENGINE=MyISAM AUTO_INCREMENT=94 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add permission',1,'add_permission'),(2,'Can change permission',1,'change_permission'),(3,'Can delete permission',1,'delete_permission'),(4,'Can add group',2,'add_group'),(5,'Can change group',2,'change_group'),(6,'Can delete group',2,'delete_group'),(7,'Can add user',3,'add_user'),(8,'Can change user',3,'change_user'),(9,'Can delete user',3,'delete_user'),(10,'Can add content type',4,'add_contenttype'),(11,'Can change content type',4,'change_contenttype'),(12,'Can delete content type',4,'delete_contenttype'),(13,'Can add session',5,'add_session'),(14,'Can change session',5,'change_session'),(15,'Can delete session',5,'delete_session'),(16,'Can add site',6,'add_site'),(17,'Can change site',6,'change_site'),(18,'Can delete site',6,'delete_site'),(19,'Can add course type',7,'add_coursetype'),(20,'Can change course type',7,'change_coursetype'),(21,'Can delete course type',7,'delete_coursetype'),(22,'Can add administrator',8,'add_administrator'),(23,'Can change administrator',8,'change_administrator'),(24,'Can delete administrator',8,'delete_administrator'),(25,'Can add student',9,'add_student'),(26,'Can change student',9,'change_student'),(27,'Can delete student',9,'delete_student'),(28,'Can add teacher',10,'add_teacher'),(29,'Can change teacher',10,'change_teacher'),(30,'Can delete teacher',10,'delete_teacher'),(31,'Can add task',11,'add_task'),(32,'Can change task',11,'change_task'),(33,'Can delete task',11,'delete_task'),(34,'Can add question',12,'add_question'),(35,'Can change question',12,'change_question'),(36,'Can delete question',12,'delete_question'),(37,'Can add answer question',13,'add_answerquestion'),(38,'Can change answer question',13,'change_answerquestion'),(39,'Can delete answer question',13,'delete_answerquestion'),(40,'Can add topic',14,'add_topic'),(41,'Can change topic',14,'change_topic'),(42,'Can delete topic',14,'delete_topic'),(43,'Can add topic reply',15,'add_topicreply'),(44,'Can change topic reply',15,'change_topicreply'),(45,'Can delete topic reply',15,'delete_topicreply'),(46,'Can add course',16,'add_course'),(47,'Can change course',16,'change_course'),(48,'Can delete course',16,'delete_course'),(49,'Can add resource',17,'add_resource'),(50,'Can change resource',17,'change_resource'),(51,'Can delete resource',17,'delete_resource'),(52,'Can add course notice',18,'add_coursenotice'),(53,'Can change course notice',18,'change_coursenotice'),(54,'Can delete course notice',18,'delete_coursenotice'),(55,'Can add course comment',19,'add_coursecomment'),(56,'Can change course comment',19,'change_coursecomment'),(57,'Can delete course comment',19,'delete_coursecomment'),(58,'Can add course note',20,'add_coursenote'),(59,'Can change course note',20,'change_coursenote'),(60,'Can delete course note',20,'delete_coursenote'),(61,'Can add exercise type',21,'add_exercisetype'),(62,'Can change exercise type',21,'change_exercisetype'),(63,'Can delete exercise type',21,'delete_exercisetype'),(64,'Can add exercise',22,'add_exercise'),(65,'Can change exercise',22,'change_exercise'),(66,'Can delete exercise',22,'delete_exercise'),(67,'Can add exercise paper',23,'add_exercisepaper'),(68,'Can change exercise paper',23,'change_exercisepaper'),(69,'Can delete exercise paper',23,'delete_exercisepaper'),(70,'Can add exercise paper detail',24,'add_exercisepaperdetail'),(71,'Can change exercise paper detail',24,'change_exercisepaperdetail'),(72,'Can delete exercise paper detail',24,'delete_exercisepaperdetail'),(73,'Can add exam',25,'add_exam'),(74,'Can change exam',25,'change_exam'),(75,'Can delete exam',25,'delete_exam'),(76,'Can add exam detail',26,'add_examdetail'),(77,'Can change exam detail',26,'change_examdetail'),(78,'Can delete exam detail',26,'delete_examdetail'),(79,'Can add exam situation',27,'add_examsituation'),(80,'Can change exam situation',27,'change_examsituation'),(81,'Can delete exam situation',27,'delete_examsituation'),(82,'Can add learn',28,'add_learn'),(83,'Can change learn',28,'change_learn'),(84,'Can delete learn',28,'delete_learn'),(85,'Can add learn detail',29,'add_learndetail'),(86,'Can change learn detail',29,'change_learndetail'),(87,'Can delete learn detail',29,'delete_learndetail'),(88,'Can add course learning',30,'add_courselearning'),(89,'Can change course learning',30,'change_courselearning'),(90,'Can delete course learning',30,'delete_courselearning'),(91,'Can add task learning',31,'add_tasklearning'),(92,'Can change task learning',31,'change_tasklearning'),(93,'Can delete task learning',31,'delete_tasklearning');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(75) NOT NULL,
  `password` varchar(128) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `last_login` datetime NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'yiranyaoqiu','','','1491634755@qq.com','pbkdf2_sha256$10000$WZT8doGZoxq2$xrtrhCc9Z1wcuQvy3BwJH8byqmctJECeNx5jq/1nCvU=',1,1,1,'2014-03-17 15:33:19','2014-03-17 15:33:19');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`group_id`),
  KEY `auth_user_groups_fbfc09f1` (`user_id`),
  KEY `auth_user_groups_bda51c3c` (`group_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`permission_id`),
  KEY `auth_user_user_permissions_fbfc09f1` (`user_id`),
  KEY `auth_user_user_permissions_1e014c8f` (`permission_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `contact_answerquestion`
--

DROP TABLE IF EXISTS `contact_answerquestion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `contact_answerquestion` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `answerquestion_content` varchar(500) NOT NULL,
  `answerquestion_userid` int(11) NOT NULL,
  `answerquestion_usertype` int(11) NOT NULL,
  `answerquestion_time` datetime NOT NULL,
  `answerquestion_status` tinyint(1) NOT NULL,
  `question_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `contact_answerquestion_1f92e550` (`question_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contact_answerquestion`
--

LOCK TABLES `contact_answerquestion` WRITE;
/*!40000 ALTER TABLE `contact_answerquestion` DISABLE KEYS */;
/*!40000 ALTER TABLE `contact_answerquestion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `contact_question`
--

DROP TABLE IF EXISTS `contact_question`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `contact_question` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `question_title` varchar(100) NOT NULL,
  `student_id` int(11) NOT NULL,
  `question_starttime` datetime NOT NULL,
  `question_status` tinyint(1) NOT NULL,
  `question_content` varchar(500) NOT NULL,
  `course_id` int(11) NOT NULL,
  `question_viewtimes` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `contact_question_42ff452e` (`student_id`),
  KEY `contact_question_ff48d8e5` (`course_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contact_question`
--

LOCK TABLES `contact_question` WRITE;
/*!40000 ALTER TABLE `contact_question` DISABLE KEYS */;
/*!40000 ALTER TABLE `contact_question` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `contact_topic`
--

DROP TABLE IF EXISTS `contact_topic`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `contact_topic` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `topic_title` varchar(100) NOT NULL,
  `topic_content` varchar(500) NOT NULL,
  `topic_userid` int(11) NOT NULL,
  `topic_status` tinyint(1) NOT NULL,
  `course_id` int(11) NOT NULL,
  `topic_usertype` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `contact_topic_ff48d8e5` (`course_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contact_topic`
--

LOCK TABLES `contact_topic` WRITE;
/*!40000 ALTER TABLE `contact_topic` DISABLE KEYS */;
/*!40000 ALTER TABLE `contact_topic` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `contact_topicreply`
--

DROP TABLE IF EXISTS `contact_topicreply`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `contact_topicreply` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `topicreply_isreply` tinyint(1) NOT NULL,
  `topicreply_content` varchar(500) NOT NULL,
  `topicreply_replyid` int(11) NOT NULL,
  `topicreply_userid` int(11) NOT NULL,
  `topicreply_status` tinyint(1) NOT NULL,
  `topicreply_time` datetime NOT NULL,
  `topic_id` int(11) NOT NULL,
  `topicreply_usertype` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `contact_topicreply_57732028` (`topic_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contact_topicreply`
--

LOCK TABLES `contact_topicreply` WRITE;
/*!40000 ALTER TABLE `contact_topicreply` DISABLE KEYS */;
/*!40000 ALTER TABLE `contact_topicreply` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `course_course`
--

DROP TABLE IF EXISTS `course_course`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `course_course` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `course_name` varchar(100) NOT NULL,
  `course_description` varchar(500) NOT NULL,
  `course_tags` varchar(50) NOT NULL,
  `course_icon` varchar(100) NOT NULL,
  `teacher_id` int(11) NOT NULL,
  `course_lessonnum` int(11) DEFAULT NULL,
  `course_outline` varchar(500) DEFAULT NULL,
  `course_credit` int(11) NOT NULL,
  `course_learner` varchar(50) DEFAULT NULL,
  `course_status` tinyint(1) NOT NULL,
  `coursetype_id` int(11) NOT NULL,
  `course_ischecked` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `course_course_e9e1ea3d` (`teacher_id`),
  KEY `course_course_54fb2301` (`coursetype_id`)
) ENGINE=MyISAM AUTO_INCREMENT=33 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `course_course`
--

LOCK TABLES `course_course` WRITE;
/*!40000 ALTER TABLE `course_course` DISABLE KEYS */;
INSERT INTO `course_course` VALUES (32,'核心编程','asdf','算法','photo/course/123.jpeg',1,NULL,'asdf',12,'教师',0,3,0),(31,'核心编程','qwer','啊啊啊啊-啊啊啊-','photo/course/Screenshot-2014-03-16_214735.png',1,NULL,'qwer',2,'教师',0,4,0);
/*!40000 ALTER TABLE `course_course` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `course_coursecomment`
--

DROP TABLE IF EXISTS `course_coursecomment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `course_coursecomment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `coursecomment_userid` int(11) NOT NULL,
  `coursecomment_usertype` int(11) NOT NULL,
  `coursecomment_score` int(11) DEFAULT NULL,
  `coursecomment_content` varchar(500) NOT NULL,
  `coursecomment_status` tinyint(1) NOT NULL,
  `course_id` int(11) NOT NULL,
  `coursecomment_time` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `course_coursecomment_ff48d8e5` (`course_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `course_coursecomment`
--

LOCK TABLES `course_coursecomment` WRITE;
/*!40000 ALTER TABLE `course_coursecomment` DISABLE KEYS */;
/*!40000 ALTER TABLE `course_coursecomment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `course_coursenote`
--

DROP TABLE IF EXISTS `course_coursenote`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `course_coursenote` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `course_id` int(11) NOT NULL,
  `coursenote_title` varchar(100) NOT NULL,
  `coursenote_content` varchar(500) NOT NULL,
  `student_id` int(11) NOT NULL,
  `coursenote_status` tinyint(1) NOT NULL,
  `coursenote_ispublic` tinyint(1) NOT NULL,
  `coursenote_viewtimes` int(11) NOT NULL,
  `coursenote_time` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `course_coursenote_ff48d8e5` (`course_id`),
  KEY `course_coursenote_42ff452e` (`student_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `course_coursenote`
--

LOCK TABLES `course_coursenote` WRITE;
/*!40000 ALTER TABLE `course_coursenote` DISABLE KEYS */;
/*!40000 ALTER TABLE `course_coursenote` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `course_coursenotice`
--

DROP TABLE IF EXISTS `course_coursenotice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `course_coursenotice` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `course_id` int(11) NOT NULL,
  `coursenotice_title` varchar(100) NOT NULL,
  `coursenotice_content` varchar(500) NOT NULL,
  `coursenotice_status` tinyint(1) NOT NULL,
  `teacher_id` int(11) NOT NULL,
  `coursenotice_time` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `course_coursenotice_ff48d8e5` (`course_id`),
  KEY `course_coursenotice_e9e1ea3d` (`teacher_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `course_coursenotice`
--

LOCK TABLES `course_coursenotice` WRITE;
/*!40000 ALTER TABLE `course_coursenotice` DISABLE KEYS */;
/*!40000 ALTER TABLE `course_coursenotice` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `course_resource`
--

DROP TABLE IF EXISTS `course_resource`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `course_resource` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `resource_name` varchar(100) NOT NULL,
  `resource_size` decimal(5,2) DEFAULT NULL,
  `resource_uploader` varchar(30) NOT NULL,
  `course_id` int(11) NOT NULL,
  `resource_iscourseware` tinyint(1) NOT NULL,
  `resource_candownload` tinyint(1) NOT NULL,
  `resource_tags` varchar(50) NOT NULL,
  `resource_standardtime` int(11) DEFAULT NULL,
  `resource_viewtimes` int(11) NOT NULL,
  `resource_downloadtimes` int(11) NOT NULL,
  `resource_status` tinyint(1) NOT NULL,
  `resource_path` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `course_resource_ff48d8e5` (`course_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `course_resource`
--

LOCK TABLES `course_resource` WRITE;
/*!40000 ALTER TABLE `course_resource` DISABLE KEYS */;
/*!40000 ALTER TABLE `course_resource` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `app_label` (`app_label`,`model`)
) ENGINE=MyISAM AUTO_INCREMENT=32 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'permission','auth','permission'),(2,'group','auth','group'),(3,'user','auth','user'),(4,'content type','contenttypes','contenttype'),(5,'session','sessions','session'),(6,'site','sites','site'),(7,'course type','admin','coursetype'),(8,'administrator','admin','administrator'),(9,'student','admin','student'),(10,'teacher','admin','teacher'),(11,'task','admin','task'),(12,'question','contact','question'),(13,'answer question','contact','answerquestion'),(14,'topic','contact','topic'),(15,'topic reply','contact','topicreply'),(16,'course','course','course'),(17,'resource','course','resource'),(18,'course notice','course','coursenotice'),(19,'course comment','course','coursecomment'),(20,'course note','course','coursenote'),(21,'exercise type','exam','exercisetype'),(22,'exercise','exam','exercise'),(23,'exercise paper','exam','exercisepaper'),(24,'exercise paper detail','exam','exercisepaperdetail'),(25,'exam','exam','exam'),(26,'exam detail','exam','examdetail'),(27,'exam situation','exam','examsituation'),(28,'learn','learn','learn'),(29,'learn detail','learn','learndetail'),(30,'course learning','learn','courselearning'),(31,'task learning','learn','tasklearning');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_c25c2c28` (`expire_date`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_site`
--

DROP TABLE IF EXISTS `django_site`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_site` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `domain` varchar(100) NOT NULL,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_site`
--

LOCK TABLES `django_site` WRITE;
/*!40000 ALTER TABLE `django_site` DISABLE KEYS */;
INSERT INTO `django_site` VALUES (1,'example.com','example.com');
/*!40000 ALTER TABLE `django_site` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `exam_exam`
--

DROP TABLE IF EXISTS `exam_exam`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `exam_exam` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `student_id` int(11) NOT NULL,
  `exam_scores` int(11) NOT NULL,
  `exercisepaper_id` int(11) NOT NULL,
  `exam_starttime` datetime NOT NULL,
  `exam_endtime` datetime NOT NULL,
  `exam_status` tinyint(1) NOT NULL,
  `exam_markingstatus` tinyint(1) NOT NULL,
  `exam_remark` varchar(500) DEFAULT NULL,
  `exam_ispassed` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `exam_exam_42ff452e` (`student_id`),
  KEY `exam_exam_45fe8337` (`exercisepaper_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exam_exam`
--

LOCK TABLES `exam_exam` WRITE;
/*!40000 ALTER TABLE `exam_exam` DISABLE KEYS */;
/*!40000 ALTER TABLE `exam_exam` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `exam_examdetail`
--

DROP TABLE IF EXISTS `exam_examdetail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `exam_examdetail` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `exam_id` int(11) NOT NULL,
  `exercise_id` int(11) NOT NULL,
  `examdetail_answeritem` varchar(10) DEFAULT NULL,
  `examdetail_answercontent` varchar(500) DEFAULT NULL,
  `examdetail_iscorrect` tinyint(1) NOT NULL,
  `examdetail_answerscore` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `exam_examdetail_6b01437f` (`exam_id`),
  KEY `exam_examdetail_d866451e` (`exercise_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exam_examdetail`
--

LOCK TABLES `exam_examdetail` WRITE;
/*!40000 ALTER TABLE `exam_examdetail` DISABLE KEYS */;
/*!40000 ALTER TABLE `exam_examdetail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `exam_examsituation`
--

DROP TABLE IF EXISTS `exam_examsituation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `exam_examsituation` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `exam_id` int(11) NOT NULL,
  `examsituation_times` int(11) NOT NULL,
  `examsituation_ispassed` tinyint(1) NOT NULL,
  `examsituation_highestscore` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `exam_examsituation_6b01437f` (`exam_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exam_examsituation`
--

LOCK TABLES `exam_examsituation` WRITE;
/*!40000 ALTER TABLE `exam_examsituation` DISABLE KEYS */;
/*!40000 ALTER TABLE `exam_examsituation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `exam_exercise`
--

DROP TABLE IF EXISTS `exam_exercise`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `exam_exercise` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `exercisetype_id` int(11) NOT NULL,
  `exercise_title` varchar(200) NOT NULL,
  `exercise_itema` varchar(100) DEFAULT NULL,
  `exercise_itemb` varchar(100) DEFAULT NULL,
  `exercise_itemc` varchar(100) DEFAULT NULL,
  `exercise_itemd` varchar(100) DEFAULT NULL,
  `exercise_correctitem` varchar(50) DEFAULT NULL,
  `exercise_resolution` varchar(200) DEFAULT NULL,
  `exercise_status` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `exam_exercise_264423a` (`exercisetype_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exam_exercise`
--

LOCK TABLES `exam_exercise` WRITE;
/*!40000 ALTER TABLE `exam_exercise` DISABLE KEYS */;
/*!40000 ALTER TABLE `exam_exercise` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `exam_exercisepaper`
--

DROP TABLE IF EXISTS `exam_exercisepaper`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `exam_exercisepaper` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `exercisepaper_name` varchar(50) NOT NULL,
  `exercisepaper_allscore` int(11) DEFAULT NULL,
  `exercisepaper_passedscore` int(11) DEFAULT NULL,
  `exercisepaper_lasttime` int(11) NOT NULL,
  `exercise_starttime` datetime NOT NULL,
  `exercise_endtime` datetime NOT NULL,
  `exercise_status` tinyint(1) NOT NULL,
  `exercise_ischecked` tinyint(1) NOT NULL,
  `course_id` int(11) NOT NULL,
  `exercise_exercisecount` int(11) DEFAULT NULL,
  `exercise_examtimes` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `exam_exercisepaper_ff48d8e5` (`course_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exam_exercisepaper`
--

LOCK TABLES `exam_exercisepaper` WRITE;
/*!40000 ALTER TABLE `exam_exercisepaper` DISABLE KEYS */;
/*!40000 ALTER TABLE `exam_exercisepaper` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `exam_exercisepaperdetail`
--

DROP TABLE IF EXISTS `exam_exercisepaperdetail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `exam_exercisepaperdetail` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `exercise_id` int(11) NOT NULL,
  `exercisepaper_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `exam_exercisepaperdetail_d866451e` (`exercise_id`),
  KEY `exam_exercisepaperdetail_45fe8337` (`exercisepaper_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exam_exercisepaperdetail`
--

LOCK TABLES `exam_exercisepaperdetail` WRITE;
/*!40000 ALTER TABLE `exam_exercisepaperdetail` DISABLE KEYS */;
/*!40000 ALTER TABLE `exam_exercisepaperdetail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `exam_exercisetype`
--

DROP TABLE IF EXISTS `exam_exercisetype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `exam_exercisetype` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `exercise_name` varchar(20) NOT NULL,
  `exercise_score` int(11) NOT NULL,
  `exercise_status` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exam_exercisetype`
--

LOCK TABLES `exam_exercisetype` WRITE;
/*!40000 ALTER TABLE `exam_exercisetype` DISABLE KEYS */;
/*!40000 ALTER TABLE `exam_exercisetype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `learn_courselearning`
--

DROP TABLE IF EXISTS `learn_courselearning`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `learn_courselearning` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `course_id` int(11) NOT NULL,
  `courselearning_status` int(11) NOT NULL,
  `courselearning_credit` int(11) NOT NULL,
  `courselearning_rate` int(11) NOT NULL,
  `student_id` int(11) NOT NULL,
  `task_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `learn_courselearning_ff48d8e5` (`course_id`),
  KEY `learn_courselearning_42ff452e` (`student_id`),
  KEY `learn_courselearning_c00fe455` (`task_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `learn_courselearning`
--

LOCK TABLES `learn_courselearning` WRITE;
/*!40000 ALTER TABLE `learn_courselearning` DISABLE KEYS */;
/*!40000 ALTER TABLE `learn_courselearning` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `learn_learn`
--

DROP TABLE IF EXISTS `learn_learn`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `learn_learn` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `course_id` int(11) NOT NULL,
  `resource_id` int(11) NOT NULL,
  `student_id` int(11) NOT NULL,
  `learn_times` int(11) NOT NULL,
  `learn_rate` int(11) NOT NULL,
  `learn_status` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `learn_learn_ff48d8e5` (`course_id`),
  KEY `learn_learn_31b73438` (`resource_id`),
  KEY `learn_learn_42ff452e` (`student_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `learn_learn`
--

LOCK TABLES `learn_learn` WRITE;
/*!40000 ALTER TABLE `learn_learn` DISABLE KEYS */;
/*!40000 ALTER TABLE `learn_learn` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `learn_learndetail`
--

DROP TABLE IF EXISTS `learn_learndetail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `learn_learndetail` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `learn_id` int(11) NOT NULL,
  `learn_starttime` datetime NOT NULL,
  `learn_endtime` datetime DEFAULT NULL,
  `learn_timelength` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `learn_learndetail_d6ae1c01` (`learn_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `learn_learndetail`
--

LOCK TABLES `learn_learndetail` WRITE;
/*!40000 ALTER TABLE `learn_learndetail` DISABLE KEYS */;
/*!40000 ALTER TABLE `learn_learndetail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `learn_tasklearning`
--

DROP TABLE IF EXISTS `learn_tasklearning`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `learn_tasklearning` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `student_id` int(11) NOT NULL,
  `tasklearning_status` int(11) NOT NULL,
  `tasklearning_score` int(11) NOT NULL,
  `task_id` int(11) NOT NULL,
  `tasklearning_rate` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `learn_tasklearning_42ff452e` (`student_id`),
  KEY `learn_tasklearning_c00fe455` (`task_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `learn_tasklearning`
--

LOCK TABLES `learn_tasklearning` WRITE;
/*!40000 ALTER TABLE `learn_tasklearning` DISABLE KEYS */;
/*!40000 ALTER TABLE `learn_tasklearning` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2014-03-23 22:33:02
