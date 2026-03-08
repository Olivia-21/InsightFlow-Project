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
public class StoreDto {
    private Integer storeId;
    private String storeName;
    private String email;
    private String phone;
    private String address;
    private LocalDateTime createdAt;
}
