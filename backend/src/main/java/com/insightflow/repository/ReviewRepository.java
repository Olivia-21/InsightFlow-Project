package com.insightflow.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import com.insightflow.model.Review;

public interface ReviewRepository extends JpaRepository<Review, Integer> {
    
    List<Review> findByProductProductId(Integer productId);
    
    List<Review> findByUsersUserId(Integer userId);
    
    List<Review> findByRating(Integer rating);
    
    @Query("SELECT r FROM Review r WHERE r.product.productId = :productId AND r.rating >= :minRating")
    List<Review> findByProductIdAndMinRating(@Param("productId") Integer productId, @Param("minRating") Integer minRating);
    
    @Query("SELECT r FROM Review r WHERE r.product.productId = :productId ORDER BY r.reviewDate DESC")
    List<Review> findByProductIdOrderByDateDesc(@Param("productId") Integer productId);
    
    @Query("SELECT AVG(r.rating) FROM Review r WHERE r.product.productId = :productId")
    Double getAverageRatingForProduct(@Param("productId") Integer productId);
    
    @Query("SELECT COUNT(r) FROM Review r WHERE r.product.productId = :productId")
    Long countByProductId(@Param("productId") Integer productId);
    
    @Query("SELECT r FROM Review r WHERE r.product.store.storeId = :storeId")
    List<Review> findByStoreId(@Param("storeId") Integer storeId);
    
    @Query("SELECT AVG(r.rating) FROM Review r WHERE r.product.store.storeId = :storeId")
    Double getAverageRatingForStore(@Param("storeId") Integer storeId);
    
    @Query("SELECT COUNT(r) FROM Review r WHERE r.product.store.storeId = :storeId")
    Long countByStoreId(@Param("storeId") Integer storeId);
}
