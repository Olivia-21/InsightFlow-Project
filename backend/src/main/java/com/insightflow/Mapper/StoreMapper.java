package com.insightflow.mapper;

import java.util.List;

import org.mapstruct.BeanMapping;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.MappingTarget;
import org.mapstruct.NullValuePropertyMappingStrategy;
import org.mapstruct.ReportingPolicy;

import com.insightflow.dto.StoreDto;
import com.insightflow.model.Store;

@Mapper(componentModel = "spring", unmappedTargetPolicy = ReportingPolicy.IGNORE)
public interface StoreMapper {

    StoreDto toDto(Store store);

    @Mapping(target = "products", ignore = true)
    @Mapping(target = "inventories", ignore = true)
    Store toEntity(StoreDto dto);

    List<StoreDto> toDtoList(List<Store> stores);

    @BeanMapping(nullValuePropertyMappingStrategy = NullValuePropertyMappingStrategy.IGNORE)
    @Mapping(target = "products", ignore = true)
    @Mapping(target = "inventories", ignore = true)
    @Mapping(target = "storeId", ignore = true)
    @Mapping(target = "createdAt", ignore = true)
    void updateEntityFromDto(StoreDto dto, @MappingTarget Store entity);
}
