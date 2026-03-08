package com.insightflow.mapper;

import java.util.List;

import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.ReportingPolicy;

import com.insightflow.dto.OrderDto;
import com.insightflow.dto.OrderItemDto;
import com.insightflow.model.Order;
import com.insightflow.model.OrderItem;

@Mapper(componentModel = "spring", unmappedTargetPolicy = ReportingPolicy.IGNORE)
public interface OrderMapper {

    @Mapping(source = "users.userId", target = "userId")
    @Mapping(source = "users.name", target = "userName")
    @Mapping(source = "orderItems", target = "items")
    OrderDto toDto(Order order);

    @Mapping(target = "users", ignore = true)
    @Mapping(target = "orderItems", ignore = true)
    Order toEntity(OrderDto dto);

    @Mapping(source = "product.productId", target = "productId")
    @Mapping(source = "product.name", target = "productName")
    OrderItemDto toItemDto(OrderItem orderItem);

    List<OrderItemDto> toItemDtoList(List<OrderItem> orderItems);
    
    List<OrderDto> toDtoList(List<Order> orders);
}
