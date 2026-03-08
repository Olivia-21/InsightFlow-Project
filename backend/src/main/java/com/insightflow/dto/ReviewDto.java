package com.insightflow.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class ReviewDto {
    private Integer reviewId;
    private Integer userId;
    private Integer productId;
    private String productName;
    private Integer storeId;
    private String storeName;
    private Integer rating;
    private String comment;
    private LocalDateTime reviewDate;
}
