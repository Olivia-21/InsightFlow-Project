package com.insightflow.mapper;

import java.util.List;

import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.ReportingPolicy;

import com.insightflow.dto.ProductSummaryDto;
import com.insightflow.model.Product;

@Mapper(componentModel = "spring", unmappedTargetPolicy = ReportingPolicy.IGNORE)
public interface ProductMapper {

    // Basic mapping for Product entity
    // Can be extended with ProductDto once created
    
    @Mapping(source = "category.categoryId", target = "categoryId")
    @Mapping(source = "store.storeId", target = "storeId")
    ProductSummaryDto toSummaryDto(Product product);

    @Mapping(target = "category", ignore = true)
    @Mapping(target = "store", ignore = true)
    @Mapping(target = "inventories", ignore = true)
    @Mapping(target = "orderItems", ignore = true)
    @Mapping(target = "cartItems", ignore = true)
    @Mapping(target = "reviews", ignore = true)
    Product toEntity(ProductSummaryDto dto);

    List<ProductSummaryDto> toSummaryDtoList(List<Product> products);
}
