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
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders` (
  `OrderID` int NOT NULL AUTO_INCREMENT,
  `Cust_PhoneNumber` varchar(15) DEFAULT NULL,
  `Cust_HomeAddress` varchar(500) DEFAULT NULL,
  `Note` varchar(500) DEFAULT NULL,
  `Time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `Delivery_Status` varchar(50) DEFAULT 'Not Delivered',
  PRIMARY KEY (`OrderID`),
  KEY `Cust_PhoneNumber` (`Cust_PhoneNumber`),
  CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`Cust_PhoneNumber`) REFERENCES `customers` (`Cust_PhoneNumber`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders`
--

LOCK TABLES `orders` WRITE;
/*!40000 ALTER TABLE `orders` DISABLE KEYS */;
INSERT INTO `orders` VALUES (1,'123','A1202, Palm Springs','Call me before you come and please come between 10am-7pm','2023-10-12 15:05:56','Not Delivered'),(2,'123','aubefunafi','aiuefbi','2023-10-13 03:16:38','Not Delivered'),(3,'123','aindianefiwnrgvi','lol lmao ded','2023-10-13 12:51:57','Not Delivered'),(4,'123','auefgbwsgr','lollmaodead x2','2023-10-13 12:53:28','Not Delivered'),(5,'123','aihfiuvhb','sviub','2023-10-13 12:54:42','Not Delivered'),(6,'123','aifn','usbvs','2023-10-13 12:55:40','Not Delivered'),(7,'123','qiafiabgai','dusbgseg','2023-10-13 13:35:42','Not Delivered'),(8,'123','sgnib','gsebg','2023-10-13 13:36:25','Not Delivered'),(9,'1234','SATYAM HARMONY','jaldi bhej dena bhaiya','2023-10-28 15:05:51','Not Delivered'),(16,'123','AINFIFN','IDK?','2023-11-13 13:18:13','Not Delivered'),(19,'123','sdbgusgn','iwnrgisng','2023-11-13 14:50:59','Not Delivered'),(20,'123','swghusg','iwngsg','2023-11-13 14:51:42','Not Delivered'),(22,'123','usdgnsdg','sugnsidg','2023-11-13 14:57:58','Not Delivered'),(23,'123','sdgnuagb','sgdbub','2023-11-13 14:58:47','Not Delivered'),(24,'123','sighig','gsieghseg','2023-11-13 15:01:10','Not Delivered'),(25,'123','ihgaiahg','siegnsieg','2023-11-13 15:01:48','Not Delivered'),(26,'123','eignsig','SUDGNSE','2023-11-13 15:02:44','Not Delivered'),(27,'123','saiudgniusag','biusengsige','2023-11-13 15:03:02','Not Delivered'),(28,'9967014484','A1202, Palm Springs, Sector 7, Airoli','','2023-11-14 10:33:17','Not Delivered'),(29,'9967014484','A1202, Palm Springs, Sector 7, Airoli','NA','2023-11-14 10:46:14','Not Delivered');
/*!40000 ALTER TABLE `orders` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-11-24 10:54:36
