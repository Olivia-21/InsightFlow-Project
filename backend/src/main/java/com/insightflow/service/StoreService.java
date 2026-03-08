package com.insightflow.service;

import java.util.List;
import java.util.stream.Collectors;

import org.springframework.stereotype.Service;

import com.insightflow.dto.StoreDto;
import com.insightflow.mapper.StoreMapper;
import com.insightflow.model.Store;
import com.insightflow.repository.StoreRepository;

import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class StoreService {

    private final StoreRepository storeRepository;
    private final StoreMapper storeMapper;

    public List<StoreDto> findAll() {
        return storeRepository.findAll().stream()
                .map(storeMapper::toDto)
                .collect(Collectors.toList());
    }

    public StoreDto findById(Integer id) {
        Store store = storeRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Store not found with id: " + id));
        return storeMapper.toDto(store);
    }

    public StoreDto findByEmail(String email) {
        Store store = storeRepository.findByEmail(email)
                .orElseThrow(() -> new RuntimeException("Store not found with email: " + email));
        return storeMapper.toDto(store);
    }

    public List<StoreDto> searchByName(String name) {
        return storeRepository.searchByName(name).stream()
                .map(storeMapper::toDto)
                .collect(Collectors.toList());
    }

    public StoreDto create(StoreDto dto) {
        if (dto.getEmail() != null && storeRepository.existsByEmail(dto.getEmail())) {
            throw new RuntimeException("Email already registered: " + dto.getEmail());
        }
        Store store = storeMapper.toEntity(dto);
        return storeMapper.toDto(storeRepository.save(store));
    }

    public StoreDto update(Integer id, StoreDto dto) {
        Store store = storeRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Store not found with id: " + id));
        storeMapper.updateEntityFromDto(dto, store);
        return storeMapper.toDto(storeRepository.save(store));
    }

    public void delete(Integer id) {
        if (!storeRepository.existsById(id)) {
            throw new RuntimeException("Store not found with id: " + id);
        }
        storeRepository.deleteById(id);
    }

    public boolean existsByEmail(String email) {
        return storeRepository.existsByEmail(email);
    }
}
