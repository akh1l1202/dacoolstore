-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: dacoolstore
-- ------------------------------------------------------
-- Server version	8.0.34

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `customers`
--

DROP TABLE IF EXISTS `customers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customers` (
  `Cust_ID` int NOT NULL AUTO_INCREMENT,
  `Cust_Name` varchar(255) DEFAULT NULL,
  `Cust_Gender` tinytext,
  `Cust_EmailAddress` varchar(255) DEFAULT NULL,
  `Cust_PhoneNumber` varchar(15) DEFAULT NULL,
  `Cust_Password` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`Cust_ID`),
  UNIQUE KEY `Cust_PhoneNumber` (`Cust_PhoneNumber`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customers`
--

LOCK TABLES `customers` WRITE;
/*!40000 ALTER TABLE `customers` DISABLE KEYS */;
INSERT INTO `customers` VALUES (1,'wefiubwirbgv','Female','iwbgib.com','123','123'),(2,'wiebfwub','Female','u3bgru','996701448','lol'),(3,'iwhegiibs','Male','iwe4hgieb','678','678'),(4,'wefbwuebgs','Female','wuebgbgwub','subinbsibn','siegibns'),(5,'sneha','Female','idk','1234','1234'),(6,'','Male','','',''),(9,'awdbub','Female','uqb3ru','4525','aaha'),(10,'erg','Female','srgq','qrgqegb','qegwg'),(11,'wf','Male','3q4g1qg`4eg5rh425h','4b24b','rhbw5tr'),(14,'akhil','Male','tyagghg','12345','12345'),(15,'Akjakak','Female','aigianginsa','12345678','12345678'),(16,'ahusengunags','Male','afguabegiu','1212','1212'),(17,'THE GOAT','Male','iaeghaineg','1313','1313'),(18,'GOAT','Male','iwngisengise','1414','1414'),(19,'GOAT THE THIRD?','Male','siueghaieb','1515','1515'),(20,'Akhil Tyagi','Male','tyagi.akhil1202@gmail.com','9967014484','abc123');
/*!40000 ALTER TABLE `customers` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-11-18 11:26:06
