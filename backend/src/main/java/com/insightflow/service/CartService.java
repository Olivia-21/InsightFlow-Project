package com.insightflow.service;

import java.util.List;
import java.util.stream.Collectors;

import org.springframework.stereotype.Service;

import com.insightflow.dto.CartDto;
import com.insightflow.mapper.CartMapper;
import com.insightflow.model.Cart;
import com.insightflow.repository.CartRepository;

import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class CartService {

    private final CartRepository cartRepository;
    private final CartMapper cartMapper;

    public List<CartDto> findAll() {
        return cartRepository.findAll().stream()
                .map(cartMapper::toDto)
                .collect(Collectors.toList());
    }

    public CartDto findById(Integer id) {
        Cart cart = cartRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Cart not found with id: " + id));
        return cartMapper.toDto(cart);
    }

    public CartDto findByUserId(Integer userId) {
        Cart cart = cartRepository.findByUsersUserId(userId)
                .orElseThrow(() -> new RuntimeException("Cart not found for user id: " + userId));
        return cartMapper.toDto(cart);
    }

    public CartDto findByUserIdWithItems(Integer userId) {
        Cart cart = cartRepository.findByUserIdWithItems(userId)
                .orElseThrow(() -> new RuntimeException("Cart not found for user id: " + userId));
        return cartMapper.toDto(cart);
    }

    public CartDto create(CartDto dto) {
        Cart cart = cartMapper.toEntity(dto);
        return cartMapper.toDto(cartRepository.save(cart));
    }

    public void delete(Integer id) {
        if (!cartRepository.existsById(id)) {
            throw new RuntimeException("Cart not found with id: " + id);
        }
        cartRepository.deleteById(id);
    }

    public void deleteByUserId(Integer userId) {
        Cart cart = cartRepository.findByUsersUserId(userId)
                .orElseThrow(() -> new RuntimeException("Cart not found for user id: " + userId));
        cartRepository.delete(cart);
    }

    public boolean existsByUserId(Integer userId) {
        return cartRepository.existsByUsersUserId(userId);
    }
}
