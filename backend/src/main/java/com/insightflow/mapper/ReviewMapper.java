package com.insightflow.mapper;

import org.mapstruct.BeanMapping;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.MappingTarget;
import org.mapstruct.NullValuePropertyMappingStrategy;
import org.mapstruct.ReportingPolicy;

import com.insightflow.dto.ReviewDto;
import com.insightflow.model.Review;

@Mapper(componentModel = "spring", unmappedTargetPolicy = ReportingPolicy.IGNORE)
public interface ReviewMapper {

    @Mapping(source = "users.userId", target = "userId")
    @Mapping(source = "product.productId", target = "productId")
    @Mapping(source = "product.productName", target = "productName")
    @Mapping(source = "product.store.storeId", target = "storeId")
    @Mapping(source = "product.store.storeName", target = "storeName")
    ReviewDto toDto(Review review);

    @Mapping(target = "users", ignore = true)
    @Mapping(target = "product", ignore = true)
    @Mapping(target = "feedbackCategory", ignore = true)
    Review toEntity(ReviewDto reviewDto);

    @BeanMapping(nullValuePropertyMappingStrategy = NullValuePropertyMappingStrategy.IGNORE)
    void updateEntityFromDto(ReviewDto dto, @MappingTarget Review entity);
}
