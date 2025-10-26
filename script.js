// okay.html 페이지 스크립트
if (document.body.classList.contains('page-okay')) { 
    const productImage = document.getElementById('productImage');
    const colorSwatches = document.querySelectorAll('.page-okay .color-swatches .swatch'); 
    const colorSelect = document.getElementById('color-select');
    const giftSelect = document.getElementById('gift-message-select-okay'); 
    const giftText = document.getElementById('gift-message-text-okay'); 

    if (productImage && colorSwatches.length > 0 && colorSelect && giftSelect && giftText) { 
        // 색상 스와치
        colorSwatches.forEach(swatch => {
            swatch.addEventListener('mouseenter', () => {
                productImage.src = swatch.dataset.image;
                colorSwatches.forEach(s => s.classList.remove('active'));
                swatch.classList.add('active');
                colorSelect.value = swatch.dataset.colorValue; 
            });
        });

        // 색상 드롭다운
        colorSelect.addEventListener('change', (event) => {
            const selectedColor = event.target.value;
            const newImage = (selectedColor === 'black') ? 'okay.png' : 'okay(white).png';
            productImage.src = newImage;
            colorSwatches.forEach(s => {
                s.classList.remove('active');
                if (s.dataset.colorValue === selectedColor) {
                    s.classList.add('active');
                }
            });
        });

        // 선물 메시지 선택
        giftSelect.addEventListener('change', (event) => {
            if (event.target.value) { 
                giftText.value = event.target.value; 
            }
        });
    }
}

// keep.html 페이지 스크립트
if (document.body.classList.contains('page-keep')) {
    const productImageKeep = document.getElementById('productImageKeep');
    const productNameKeep = document.getElementById('productNameKeep');
    const productPriceKeep = document.getElementById('productPriceKeep');
    const typeSwatchesKeep = document.querySelectorAll('.page-keep .type-swatches .type-swatch');
    const colorSwatchesKeep = document.querySelectorAll('.page-keep .color-swatches .swatch'); 
    const colorSelectKeep = document.getElementById('color-select-keep');
    const productInfoWrapper = document.querySelector('.page-keep .product-info-wrapper'); 
    const productImageWrapper = document.querySelector('.page-keep .product-image-wrapper'); 
    const giftSelectKeep = document.getElementById('gift-message-select-keep'); 
    const giftTextKeep = document.getElementById('gift-message-text-keep'); 

    let currentKeepType = 'notebook'; 

    if (productImageKeep && productNameKeep && productPriceKeep && typeSwatchesKeep.length > 0 && colorSwatchesKeep.length > 0 && colorSelectKeep && productInfoWrapper && productImageWrapper && giftSelectKeep && giftTextKeep) {

        // 타입 스와치 클릭 이벤트
        typeSwatchesKeep.forEach(swatch => {
            swatch.addEventListener('click', () => { 
                currentKeepType = swatch.dataset.type; 

                typeSwatchesKeep.forEach(s => s.classList.remove('active'));
                swatch.classList.add('active');

                productNameKeep.textContent = swatch.dataset.name;
                productPriceKeep.textContent = swatch.dataset.price;

                if (currentKeepType === 'pen') {
                    productImageKeep.src = swatch.dataset.image; 
                    productInfoWrapper.classList.add('pen-selected');
                    productImageWrapper.classList.add('pen-selected'); 
                } 
                else { 
                    productInfoWrapper.classList.remove('pen-selected');
                    productImageWrapper.classList.remove('pen-selected');
                    colorSelectKeep.value = 'white'; 
                    colorSelectKeep.dispatchEvent(new Event('change')); 
                }
            });
        });

        // 색상 스와치 마우스오버 이벤트
        colorSwatchesKeep.forEach(swatch => {
            swatch.addEventListener('mouseenter', () => {
                if (currentKeepType === 'notebook') { 
                    productImageKeep.src = swatch.dataset.image;
                    colorSwatchesKeep.forEach(s => s.classList.remove('active'));
                    swatch.classList.add('active');
                    colorSelectKeep.value = swatch.dataset.colorValue; 
                }
            });
        });

        // 색상 선택 드롭다운 변경 이벤트
        colorSelectKeep.addEventListener('change', (event) => {
            if (currentKeepType === 'notebook') { 
                const selectedColor = event.target.value;
                let newImage = '';
                if (selectedColor === 'white') {
                    newImage = 'keepwhite.png';
                } else if (selectedColor === 'gray') {
                    newImage = 'keepgray.png';
                }
                
                if (newImage) { 
                    productImageKeep.src = newImage;
                }
                
                colorSwatchesKeep.forEach(s => {
                    s.classList.remove('active');
                    if (s.dataset.colorValue === selectedColor) {
                        s.classList.add('active');
                    }
                });
            }
        });

        // 선물 메시지 선택
        giftSelectKeep.addEventListener('change', (event) => {
            if (event.target.value) { 
                giftTextKeep.value = event.target.value; 
            }
        });

        // 초기 로드 시 노트북 상태로 색상 설정
        if (currentKeepType === 'notebook') {
             colorSelectKeep.value = 'white'; 
             colorSelectKeep.dispatchEvent(new Event('change'));
        }

    } // end if elements exist
} 

// with.html 페이지 스크립트
if (document.body.classList.contains('page-with')) {
    const giftSelectWith = document.getElementById('gift-message-select-with'); 
    const giftTextWith = document.getElementById('gift-message-text-with'); 

    if (giftSelectWith && giftTextWith) {
        // 선물 메시지 선택
        giftSelectWith.addEventListener('change', (event) => {
            if (event.target.value) { 
                giftTextWith.value = event.target.value; 
            }
        });
    }
}