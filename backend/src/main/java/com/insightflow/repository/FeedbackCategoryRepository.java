package com.insightflow.repository;

import com.insightflow.model.FeedbackCategory;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import java.util.List;
import java.util.Optional;

public interface FeedbackCategoryRepository extends JpaRepository<FeedbackCategory, Integer> {
    
    Optional<FeedbackCategory> findByCategoryName(String categoryName);
    
    @Query("SELECT fc FROM FeedbackCategory fc WHERE LOWER(fc.categoryName) LIKE LOWER(CONCAT('%', :name, '%'))")
    List<FeedbackCategory> searchByName(@Param("name") String name);
    
    boolean existsByCategoryName(String categoryName);
}
