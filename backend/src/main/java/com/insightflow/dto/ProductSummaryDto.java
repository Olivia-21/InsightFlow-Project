package com.insightflow.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.math.BigDecimal;
import java.time.LocalDateTime;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class ProductSummaryDto {
    private Integer productId;
    private String name;
    private String description;
    private BigDecimal price;
    private LocalDateTime createdAt;
    private Integer categoryId;
    private Integer storeId;
}
