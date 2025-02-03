-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 02, 2025 at 09:09 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `food_order`
--

-- --------------------------------------------------------

--
-- Table structure for table `menu_items`
--

CREATE TABLE `menu_items` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `description` text DEFAULT NULL,
  `image` varchar(255) DEFAULT NULL,
  `stock` int(11) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `menu_items`
--

INSERT INTO `menu_items` (`id`, `name`, `price`, `description`, `image`, `stock`, `created_at`, `updated_at`) VALUES
(1, 'Nasi Goreng', 30000.00, 'Fried rice with sunny side on top', 'https://asset.kompas.com/crops/Slbj_ngGVguffqNkbgjtdZqd8OU=/13x7:700x465/1200x800/data/photo/2021/09/24/614dc6865eb24.jpg', 15, '2025-01-27 03:41:20', '2025-01-27 04:51:43'),
(2, 'Kwetiau Goreng', 30000.00, 'Stir fried rice noodles with vegetables and chicken', 'https://asset.kompas.com/crops/99NQ5tGKFMlIBmmYNCkUHQ8YbEw=/0x0:698x465/1200x800/data/photo/2020/12/07/5fce3837c4f6d.jpg', 14, '2025-01-27 03:42:35', '2025-01-27 04:56:52'),
(3, 'Es Teh Manis', 9000.00, 'Sweet iced tea, can request sweetness level', 'https://asset.kompas.com/crops/9iB_ruTEMU7otPYnbCNVng8zhrQ=/0x0:4939x3293/1200x800/data/photo/2022/09/25/63300cfd403f0.jpg', 18, '2025-01-27 03:43:40', '2025-01-27 03:52:46');

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

CREATE TABLE `orders` (
  `id` int(11) NOT NULL,
  `customer_id` int(11) NOT NULL,
  `menu_id` int(11) NOT NULL,
  `qty` int(11) NOT NULL,
  `total` decimal(10,2) NOT NULL,
  `address` text NOT NULL,
  `status` varchar(50) NOT NULL DEFAULT 'Pending',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `orders`
--

INSERT INTO `orders` (`id`, `customer_id`, `menu_id`, `qty`, `total`, `address`, `status`, `created_at`, `updated_at`) VALUES
(1, 1, 2, 2, 30000.00, 'Jl. Teuku Umar No. 31', 'Done', '2025-01-27 03:49:49', '2025-01-27 04:39:07'),
(2, 1, 3, 2, 18000.00, 'Jl. Teuku Umar No. 13', 'Done', '2025-01-27 03:52:46', '2025-01-27 04:46:04'),
(3, 1, 1, 1, 30000.00, 'Jl. Teuku Umar No. 13', 'Done', '2025-01-27 04:16:23', '2025-01-27 04:39:31'),
(4, 1, 1, 2, 60000.00, 'Jl. Merdeka No. 1', 'Done', '2025-01-27 04:51:43', '2025-01-27 04:51:57'),
(5, 1, 2, 2, 60000.00, 'Jl. Kerumah No. 128', 'Pending', '2025-01-27 04:56:52', '2025-01-27 04:56:52');

-- --------------------------------------------------------

--
-- Table structure for table `ratings`
--

CREATE TABLE `ratings` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `menu_id` int(11) NOT NULL,
  `rating` int(11) NOT NULL,
  `feedback` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `ratings`
--

INSERT INTO `ratings` (`id`, `user_id`, `menu_id`, `rating`, `feedback`, `created_at`, `updated_at`) VALUES
(1, 1, 2, 5, 'Enak bgtt!', '2025-01-27 16:38:59', '2025-01-27 16:38:59'),
(2, 1, 3, 4, 'Kemanisan, lain kali tolong dibuat ga terlalu manis ya', '2025-01-27 17:04:54', '2025-01-27 17:04:54'),
(3, 1, 3, 5, 'Enakkk', '2025-01-27 17:06:21', '2025-01-27 17:06:21');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `full_name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` varchar(50) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `full_name`, `email`, `username`, `password`, `role`, `created_at`, `updated_at`) VALUES
(1, 'John Doe', 'johndoe@gmail.com', 'johndoe', 'scrypt:32768:8:1$7mK7NdBB0Jbja3Pg$a8c01f05993171822974092068a8b40f10a8b4ff199c44fe9ea331b5473f4ca187bf39bce3c81b926b7f10c72b55158c99d94de1ff1832ca3851e8d5a5f65980', 'user', '2025-01-27 03:39:53', '2025-01-27 03:39:53'),
(2, 'admin', 'admin@gmail.com', 'admin', 'scrypt:32768:8:1$tc3s5fxrOYhqBWZ7$565cfbf836208eb178c6d412f898b2e27bf8b6def11c02e4a70903ec7f892cf999023794a12fc9c1935f17020a4d67fc52c52230fdb507df71f867b984ccd0dc', 'admin', '2025-01-27 03:40:24', '2025-01-27 03:40:24');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `menu_items`
--
ALTER TABLE `menu_items`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`id`),
  ADD KEY `customer_id` (`customer_id`),
  ADD KEY `menu_id` (`menu_id`);

--
-- Indexes for table `ratings`
--
ALTER TABLE `ratings`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `menu_id` (`menu_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `menu_items`
--
ALTER TABLE `menu_items`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `orders`
--
ALTER TABLE `orders`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `ratings`
--
ALTER TABLE `ratings`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `orders`
--
ALTER TABLE `orders`
  ADD CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `orders_ibfk_2` FOREIGN KEY (`menu_id`) REFERENCES `menu_items` (`id`);

--
-- Constraints for table `ratings`
--
ALTER TABLE `ratings`
  ADD CONSTRAINT `ratings_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `ratings_ibfk_2` FOREIGN KEY (`menu_id`) REFERENCES `menu_items` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
