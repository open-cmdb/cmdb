-- MySQL dump 10.13  Distrib 5.7.21, for Linux (x86_64)
--
-- Host: localhost    Database: cmdb
-- ------------------------------------------------------
-- Server version	5.7.21

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
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
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
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
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=40 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add 用户',1,'add_user'),(2,'Can change 用户',1,'change_user'),(3,'Can delete 用户',1,'delete_user'),(4,'Can add 部门',2,'add_department'),(5,'Can change 部门',2,'change_department'),(6,'Can delete 部门',2,'delete_department'),(7,'Can add field',3,'add_field'),(8,'Can change field',3,'change_field'),(9,'Can delete field',3,'delete_field'),(10,'Can add 权限',4,'add_permission'),(11,'Can change 权限',4,'change_permission'),(12,'Can delete 权限',4,'delete_permission'),(13,'Can add table',5,'add_table'),(14,'Can change table',5,'change_table'),(15,'Can delete table',5,'delete_table'),(16,'Can add person',6,'add_person'),(17,'Can change person',6,'change_person'),(18,'Can delete person',6,'delete_person'),(19,'Can add test',7,'add_test'),(20,'Can change test',7,'change_test'),(21,'Can delete test',7,'delete_test'),(22,'Can add log entry',8,'add_logentry'),(23,'Can change log entry',8,'change_logentry'),(24,'Can delete log entry',8,'delete_logentry'),(25,'Can add permission',9,'add_permission'),(26,'Can change permission',9,'change_permission'),(27,'Can delete permission',9,'delete_permission'),(28,'Can add group',10,'add_group'),(29,'Can change group',10,'change_group'),(30,'Can delete group',10,'delete_group'),(31,'Can add content type',11,'add_contenttype'),(32,'Can change content type',11,'change_contenttype'),(33,'Can delete content type',11,'delete_contenttype'),(34,'Can add session',12,'add_session'),(35,'Can change session',12,'change_session'),(36,'Can delete session',12,'delete_session'),(37,'Can add rest pw verify code',13,'add_restpwverifycode'),(38,'Can change rest pw verify code',13,'change_restpwverifycode'),(39,'Can delete rest pw verify code',13,'delete_restpwverifycode');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `c_test_person`
--

DROP TABLE IF EXISTS `c_test_person`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `c_test_person` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(20) NOT NULL,
  `birth` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `c_test_person`
--

LOCK TABLES `c_test_person` WRITE;
/*!40000 ALTER TABLE `c_test_person` DISABLE KEYS */;
/*!40000 ALTER TABLE `c_test_person` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `c_test_test`
--

DROP TABLE IF EXISTS `c_test_test`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `c_test_test` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `c_test_test`
--

LOCK TABLES `c_test_test` WRITE;
/*!40000 ALTER TABLE `c_test_test` DISABLE KEYS */;
/*!40000 ALTER TABLE `c_test_test` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_mgmt_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_mgmt_user_id` FOREIGN KEY (`user_id`) REFERENCES `mgmt_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2018-09-08 20:03:19.177040','2','唐明明',2,'[{\"changed\": {\"fields\": [\"first_name\", \"name\", \"permissions\"]}}]',1,1),(2,'2018-09-23 01:14:29.669643','4','李四44',2,'[{\"changed\": {\"fields\": [\"permissions\"]}}]',1,1),(3,'2018-09-23 01:18:35.233175','1','软件研发中心',1,'[{\"added\": {}}]',2,1),(4,'2018-09-23 01:18:52.135913','2','运维',1,'[{\"added\": {}}]',2,1),(5,'2018-09-23 01:19:46.266670','4','李四44',2,'[{\"changed\": {\"fields\": [\"departments\"]}}]',1,1),(6,'2018-10-08 09:01:19.379541','4','李四44',2,'[{\"changed\": {\"fields\": [\"permissions\"]}}]',1,1),(7,'2018-10-08 09:49:27.621413','4','李四44',2,'[{\"changed\": {\"fields\": [\"permissions\"]}}]',1,1),(8,'2018-10-08 14:47:10.880123','4','李四44',2,'[{\"changed\": {\"fields\": [\"permissions\"]}}]',1,1),(9,'2018-10-13 18:58:57.606166','2','唐明明',2,'[{\"changed\": {\"fields\": [\"is_superuser\"]}}]',1,1),(10,'2018-10-13 19:07:07.815126','2','唐明明',2,'[{\"changed\": {\"fields\": [\"is_superuser\"]}}]',1,1),(11,'2018-10-13 19:07:32.740503','2','唐明明',2,'[{\"changed\": {\"fields\": [\"is_superuser\"]}}]',1,1),(12,'2018-10-13 21:54:44.991052','2','运维',3,'',2,1),(13,'2018-10-13 21:54:51.340873','1','软件研发中心',3,'',2,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (8,'admin','logentry'),(10,'auth','group'),(9,'auth','permission'),(11,'contenttypes','contenttype'),(6,'c_test','person'),(7,'c_test','test'),(2,'mgmt','department'),(3,'mgmt','field'),(4,'mgmt','permission'),(13,'mgmt','restpwverifycode'),(5,'mgmt','table'),(1,'mgmt','user'),(12,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2018-08-25 12:46:04.472488'),(2,'contenttypes','0002_remove_content_type_name','2018-08-25 12:46:04.525274'),(3,'auth','0001_initial','2018-08-25 12:46:04.690439'),(4,'auth','0002_alter_permission_name_max_length','2018-08-25 12:46:04.725921'),(5,'auth','0003_alter_user_email_max_length','2018-08-25 12:46:04.734384'),(6,'auth','0004_alter_user_username_opts','2018-08-25 12:46:04.745799'),(7,'auth','0005_alter_user_last_login_null','2018-08-25 12:46:04.754037'),(8,'auth','0006_require_contenttypes_0002','2018-08-25 12:46:04.758002'),(9,'auth','0007_alter_validators_add_error_messages','2018-08-25 12:46:04.764905'),(10,'auth','0008_alter_user_username_max_length','2018-08-25 12:46:04.773448'),(11,'mgmt','0001_initial','2018-08-25 12:46:05.382584'),(12,'admin','0001_initial','2018-08-25 12:46:05.457167'),(13,'admin','0002_logentry_remove_auto_add','2018-08-25 12:46:05.479404'),(14,'c_test','0001_initial','2018-08-25 12:46:05.509638'),(15,'sessions','0001_initial','2018-08-25 12:46:05.534076'),(16,'mgmt','0002_restpwverifycode','2018-09-08 15:57:31.965742');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
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
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('bp8zh5a4daeb18bgkwnpiajgv8w0pxn2','MmQwZjE0NjE0ZTFhYzE0MWQ2MGExYTE4ZGIzZjI3YmY5ZjRlNDk4ODp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI2Mjk3MzExNzY3NDg2ODMzNjUxNDgyNDQ4YTMzNjMxYWJjZTI1NTViIn0=','2018-09-22 19:33:02.760195'),('dt02qcdvaow3y5au3ascbxic7ix95xjy','ZWRkNDM4MjE1MzMyZGIyZmE2NjE2NTM3MjNkZjcxN2UzOWY2NjM3ZDp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIzZGIyZmZmNjlkZDFmOGM2YzViZDk5YWM2YzJiODNjYmM5ZmZlYzhkIn0=','2018-10-22 08:59:26.325989'),('ldu3scg5rax3fzexffz0g3bxy1btyy3h','ZTJmM2FmYmUzMzE5NzMzMDg2ZjgyMDllNDkzMzNkOTUzNDRkYmNjNTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJiOTIxZjdkMDhmMTE5ODZjMjNmMDYwNGVkOWExYmU4NzE3OWM3YzVkIn0=','2018-10-27 18:58:43.023359'),('oy909oltlcmfc0hhi9dyge5cyeupr5fb','ZWRkNDM4MjE1MzMyZGIyZmE2NjE2NTM3MjNkZjcxN2UzOWY2NjM3ZDp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIzZGIyZmZmNjlkZDFmOGM2YzViZDk5YWM2YzJiODNjYmM5ZmZlYzhkIn0=','2018-10-07 01:13:06.201662');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mgmt_department`
--

DROP TABLE IF EXISTS `mgmt_department`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mgmt_department` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(20) NOT NULL,
  `level` smallint(6) NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `parent_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mgmt_department_name_parent_id_ca45c293_uniq` (`name`,`parent_id`),
  KEY `mgmt_department_parent_id_8e2c8ff1_fk_mgmt_department_id` (`parent_id`),
  CONSTRAINT `mgmt_department_parent_id_8e2c8ff1_fk_mgmt_department_id` FOREIGN KEY (`parent_id`) REFERENCES `mgmt_department` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mgmt_department`
--

LOCK TABLES `mgmt_department` WRITE;
/*!40000 ALTER TABLE `mgmt_department` DISABLE KEYS */;
/*!40000 ALTER TABLE `mgmt_department` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mgmt_department_permissions`
--

DROP TABLE IF EXISTS `mgmt_department_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mgmt_department_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `department_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mgmt_department_permissi_department_id_permission_fe41137c_uniq` (`department_id`,`permission_id`),
  KEY `mgmt_department_perm_permission_id_961da470_fk_mgmt_perm` (`permission_id`),
  CONSTRAINT `mgmt_department_perm_department_id_5941bd02_fk_mgmt_depa` FOREIGN KEY (`department_id`) REFERENCES `mgmt_department` (`id`),
  CONSTRAINT `mgmt_department_perm_permission_id_961da470_fk_mgmt_perm` FOREIGN KEY (`permission_id`) REFERENCES `mgmt_permission` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mgmt_department_permissions`
--

LOCK TABLES `mgmt_department_permissions` WRITE;
/*!40000 ALTER TABLE `mgmt_department_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `mgmt_department_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mgmt_field`
--

DROP TABLE IF EXISTS `mgmt_field`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mgmt_field` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(20) NOT NULL,
  `alias` varchar(20) DEFAULT NULL,
  `readme` longtext,
  `type` smallint(6) NOT NULL,
  `is_multi` tinyint(1) NOT NULL,
  `required` tinyint(1) NOT NULL,
  `table_id` varchar(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `mgmt_field_table_id_84d986dd_fk_mgmt_table_name` (`table_id`),
  CONSTRAINT `mgmt_field_table_id_84d986dd_fk_mgmt_table_name` FOREIGN KEY (`table_id`) REFERENCES `mgmt_table` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mgmt_field`
--

LOCK TABLES `mgmt_field` WRITE;
/*!40000 ALTER TABLE `mgmt_field` DISABLE KEYS */;
/*!40000 ALTER TABLE `mgmt_field` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mgmt_permission`
--

DROP TABLE IF EXISTS `mgmt_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mgmt_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `alias` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mgmt_permission`
--

LOCK TABLES `mgmt_permission` WRITE;
/*!40000 ALTER TABLE `mgmt_permission` DISABLE KEYS */;
INSERT INTO `mgmt_permission` VALUES (1,'read_all','所有可读'),(2,'write_all','所有可写');
/*!40000 ALTER TABLE `mgmt_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mgmt_restpwverifycode`
--

DROP TABLE IF EXISTS `mgmt_restpwverifycode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mgmt_restpwverifycode` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` varchar(10) NOT NULL,
  `add_time` datetime(6) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `mgmt_restpwverifycode_user_id_6b9f5490_fk_mgmt_user_id` FOREIGN KEY (`user_id`) REFERENCES `mgmt_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mgmt_restpwverifycode`
--

LOCK TABLES `mgmt_restpwverifycode` WRITE;
/*!40000 ALTER TABLE `mgmt_restpwverifycode` DISABLE KEYS */;
/*!40000 ALTER TABLE `mgmt_restpwverifycode` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mgmt_table`
--

DROP TABLE IF EXISTS `mgmt_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mgmt_table` (
  `name` varchar(20) NOT NULL,
  `alias` varchar(20) DEFAULT NULL,
  `readme` longtext NOT NULL,
  `creation_time` datetime(6) NOT NULL,
  `creator_id` int(11) NOT NULL,
  PRIMARY KEY (`name`),
  UNIQUE KEY `alias` (`alias`),
  KEY `mgmt_table_creator_id_26131622_fk_mgmt_user_id` (`creator_id`),
  CONSTRAINT `mgmt_table_creator_id_26131622_fk_mgmt_user_id` FOREIGN KEY (`creator_id`) REFERENCES `mgmt_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mgmt_table`
--

LOCK TABLES `mgmt_table` WRITE;
/*!40000 ALTER TABLE `mgmt_table` DISABLE KEYS */;
/*!40000 ALTER TABLE `mgmt_table` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mgmt_user`
--

DROP TABLE IF EXISTS `mgmt_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mgmt_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `name` varchar(10) NOT NULL,
  `position` varchar(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mgmt_user`
--

LOCK TABLES `mgmt_user` WRITE;
/*!40000 ALTER TABLE `mgmt_user` DISABLE KEYS */;
INSERT INTO `mgmt_user` VALUES (1,'pbkdf2_sha256$36000$ELcqeR6ZhHPu$rRw5lwaFAiS7zqmyH/OA2lsDDbO+KezJBzvXqEIXn7A=','2018-10-13 18:58:43.011406',1,'admin','','','',1,1,'2018-08-25 14:37:29.023483','管理员','');
/*!40000 ALTER TABLE `mgmt_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mgmt_user_departments`
--

DROP TABLE IF EXISTS `mgmt_user_departments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mgmt_user_departments` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `department_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mgmt_user_departments_user_id_department_id_0b2e801c_uniq` (`user_id`,`department_id`),
  KEY `mgmt_user_department_department_id_0c70f6e4_fk_mgmt_depa` (`department_id`),
  CONSTRAINT `mgmt_user_department_department_id_0c70f6e4_fk_mgmt_depa` FOREIGN KEY (`department_id`) REFERENCES `mgmt_department` (`id`),
  CONSTRAINT `mgmt_user_departments_user_id_9b690638_fk_mgmt_user_id` FOREIGN KEY (`user_id`) REFERENCES `mgmt_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mgmt_user_departments`
--

LOCK TABLES `mgmt_user_departments` WRITE;
/*!40000 ALTER TABLE `mgmt_user_departments` DISABLE KEYS */;
/*!40000 ALTER TABLE `mgmt_user_departments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mgmt_user_groups`
--

DROP TABLE IF EXISTS `mgmt_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mgmt_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mgmt_user_groups_user_id_group_id_63b977ee_uniq` (`user_id`,`group_id`),
  KEY `mgmt_user_groups_group_id_684c73b8_fk_auth_group_id` (`group_id`),
  CONSTRAINT `mgmt_user_groups_group_id_684c73b8_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `mgmt_user_groups_user_id_6bc29fbd_fk_mgmt_user_id` FOREIGN KEY (`user_id`) REFERENCES `mgmt_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mgmt_user_groups`
--

LOCK TABLES `mgmt_user_groups` WRITE;
/*!40000 ALTER TABLE `mgmt_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `mgmt_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mgmt_user_permissions`
--

DROP TABLE IF EXISTS `mgmt_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mgmt_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mgmt_user_permissions_user_id_permission_id_84b31fcb_uniq` (`user_id`,`permission_id`),
  KEY `mgmt_user_permission_permission_id_bf5f8ea2_fk_mgmt_perm` (`permission_id`),
  CONSTRAINT `mgmt_user_permission_permission_id_bf5f8ea2_fk_mgmt_perm` FOREIGN KEY (`permission_id`) REFERENCES `mgmt_permission` (`id`),
  CONSTRAINT `mgmt_user_permissions_user_id_647982d6_fk_mgmt_user_id` FOREIGN KEY (`user_id`) REFERENCES `mgmt_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mgmt_user_permissions`
--

LOCK TABLES `mgmt_user_permissions` WRITE;
/*!40000 ALTER TABLE `mgmt_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `mgmt_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mgmt_user_user_permissions`
--

DROP TABLE IF EXISTS `mgmt_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mgmt_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mgmt_user_user_permissions_user_id_permission_id_bf60d734_uniq` (`user_id`,`permission_id`),
  KEY `mgmt_user_user_permi_permission_id_2f56c0ab_fk_auth_perm` (`permission_id`),
  CONSTRAINT `mgmt_user_user_permi_permission_id_2f56c0ab_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `mgmt_user_user_permissions_user_id_6463a0a6_fk_mgmt_user_id` FOREIGN KEY (`user_id`) REFERENCES `mgmt_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mgmt_user_user_permissions`
--

LOCK TABLES `mgmt_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `mgmt_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `mgmt_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-10-13 13:56:59
