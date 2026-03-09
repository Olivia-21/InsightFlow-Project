package com.insightflow.mapper;

import java.util.List;

import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.ReportingPolicy;

import com.insightflow.dto.CartDto;
import com.insightflow.dto.CartItemDto;
import com.insightflow.model.Cart;
import com.insightflow.model.CartItem;

@Mapper(componentModel = "spring", unmappedTargetPolicy = ReportingPolicy.IGNORE)
public interface CartMapper {

    @Mapping(source = "users.userId", target = "userId")
    @Mapping(source = "cartItems", target = "items")
    CartDto toDto(Cart cart);

    @Mapping(target = "users", ignore = true)
    @Mapping(target = "cartItems", ignore = true)
    Cart toEntity(CartDto dto);

    @Mapping(source = "product.productId", target = "productId")
    @Mapping(source = "product.productName", target = "productName")
    @Mapping(source = "product.unitPrice", target = "unitPrice")
    CartItemDto toItemDto(CartItem cartItem);

    List<CartItemDto> toItemDtoList(List<CartItem> cartItems);
}
