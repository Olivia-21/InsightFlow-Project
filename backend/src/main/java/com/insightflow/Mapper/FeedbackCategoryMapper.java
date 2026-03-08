package com.insightflow.mapper;

import java.util.List;

import org.mapstruct.BeanMapping;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.MappingTarget;
import org.mapstruct.NullValuePropertyMappingStrategy;
import org.mapstruct.ReportingPolicy;

import com.insightflow.dto.FeedbackCategoryDto;
import com.insightflow.model.FeedbackCategory;

@Mapper(componentModel = "spring", unmappedTargetPolicy = ReportingPolicy.IGNORE)
public interface FeedbackCategoryMapper {

    FeedbackCategoryDto toDto(FeedbackCategory category);

    @Mapping(target = "reviews", ignore = true)
    FeedbackCategory toEntity(FeedbackCategoryDto dto);

    List<FeedbackCategoryDto> toDtoList(List<FeedbackCategory> categories);

    @BeanMapping(nullValuePropertyMappingStrategy = NullValuePropertyMappingStrategy.IGNORE)
    @Mapping(target = "reviews", ignore = true)
    @Mapping(target = "feedbackCategoryId", ignore = true)
    void updateEntityFromDto(FeedbackCategoryDto dto, @MappingTarget FeedbackCategory entity);
}
