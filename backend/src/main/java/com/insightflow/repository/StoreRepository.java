package com.insightflow.repository;

import com.insightflow.model.Store;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import java.util.List;
import java.util.Optional;

public interface StoreRepository extends JpaRepository<Store, Integer> {
    
    @Query("SELECT s FROM Store s WHERE LOWER(s.storeName) LIKE LOWER(CONCAT('%', :name, '%'))")
    List<Store> searchByName(@Param("name") String name);
    
    Optional<Store> findByEmail(String email);
    
    boolean existsByEmail(String email);
}
