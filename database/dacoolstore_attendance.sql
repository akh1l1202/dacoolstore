-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: dacoolstore
-- ------------------------------------------------------
-- Server version	8.0.34

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `attendance`
--

DROP TABLE IF EXISTS `attendance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `attendance` (
  `attendanceid` int NOT NULL AUTO_INCREMENT,
  `staffid` int DEFAULT NULL,
  `staffname` varchar(255) DEFAULT NULL,
  `timestamp` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`attendanceid`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `attendance`
--

LOCK TABLES `attendance` WRITE;
/*!40000 ALTER TABLE `attendance` DISABLE KEYS */;
INSERT INTO `attendance` VALUES (2,2,'test','2023-11-16 14:57:10'),(3,2,'test','2023-11-16 14:57:30'),(4,1,'Akhil Tyagi','2023-11-16 15:04:37'),(5,2,'test','2023-11-16 15:05:18'),(6,2,'test','2023-11-16 15:06:25'),(7,1,'Akhil Tyagi','2023-11-16 15:27:02'),(8,1,'Akhil Tyagi','2023-11-16 15:30:44'),(9,1,'Akhil Tyagi','2023-11-16 15:32:44'),(10,1,'Akhil Tyagi','2023-11-16 15:33:36'),(11,1,'Akhil Tyagi','2023-11-16 15:35:19'),(12,1,'Akhil Tyagi','2023-11-16 15:38:30'),(13,1,'Akhil Tyagi','2023-11-16 15:38:54'),(14,1,'Akhil Tyagi','2023-11-16 15:39:23'),(15,1,'Akhil Tyagi','2023-11-16 15:43:08'),(16,1,'Akhil Tyagi','2023-11-16 15:44:02'),(17,1,'Akhil Tyagi','2023-11-17 16:06:41'),(18,1,'Akhil Tyagi','2023-11-18 17:04:34'),(19,1,'Akhil Tyagi','2023-11-18 17:05:00'),(20,1,'Akhil Tyagi','2023-11-18 17:05:26'),(21,1,'Akhil Tyagi','2023-11-18 17:11:31'),(22,1,'Akhil Tyagi','2023-11-18 17:12:56'),(23,1,'Akhil Tyagi','2023-11-18 17:24:32'),(24,1,'Akhil Tyagi','2023-11-18 17:25:09'),(25,2,'test','2023-11-18 17:27:09'),(26,2,'test','2023-11-18 17:30:30'),(27,2,'test','2023-11-18 17:36:31'),(28,1,'Akhil Tyagi','2023-11-22 16:53:48'),(29,1,'Akhil Tyagi','2023-11-24 05:11:56'),(30,1,'Akhil Tyagi','2023-11-24 05:20:30');
/*!40000 ALTER TABLE `attendance` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `before_attendance_insert` BEFORE INSERT ON `attendance` FOR EACH ROW BEGIN
SET NEW.staffname = (SELECT Staff_Name FROM staff WHERE Staff_ID = NEW.staffid);
SET NEW.timestamp = CURRENT_TIMESTAMP;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-11-24 10:54:36
